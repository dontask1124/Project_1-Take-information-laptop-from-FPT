
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup #Chưa áp dụng BeautifulSoup
from time import sleep
import csv
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # Chưa sử dụng Auto tải Webdriver
from selenium.webdriver.common.by import By
import pandas as pd

print("done_import")

def Lay_Ten_Laptop(ten_Laptop):
    ten = ten_Laptop.split("/")
    return ten[0]

def loc_Man_Hinh(man_Hinh):
    ts_Man_Hinh = man_Hinh.split(",")
    so_inch = ts_Man_Hinh[0][9:19]
    do_Phan_Giai = ts_Man_Hinh[1][:ts_Man_Hinh[1].find("Pixels")+len("Pixels")]
    loai_Man_Hinh = ts_Man_Hinh[2]
    khac_Man_Hinh = ts_Man_Hinh[3:]
    ts_MH_LOC =[so_inch, do_Phan_Giai, loai_Man_Hinh, khac_Man_Hinh]
    return ts_MH_LOC

def loc_CPU(CPU):
    ts_CPU =CPU.split(",")
    hang_CPU = ts_CPU[0][4:]
    
    if ("AMD","Apple","Celeron") in hang_CPU:
        dong_CPU = ts_CPU[1][1:]
    else:
        dong_CPU = ts_CPU[1][5:]
        
    loai_CPU = ts_CPU[2]
    ts_CPU_LOC = [hang_CPU, dong_CPU, loai_CPU]
    return ts_CPU_LOC

def loc_RAM(RAM):
    ts_RAM = RAM.split(",")
    dung_Luong_RAM = ts_RAM[0][4:9]
    loai_RAM = ts_RAM[1]
    so_Bus_RAM = ts_RAM[2]
    ts_RAM_LOC = [dung_Luong_RAM, loai_RAM, so_Bus_RAM]
    return ts_RAM_LOC

def lay_Tinh_Nang_Laptop(tinh_nang_Laptop, ten_Laptop,gia_Laptop):
    ten = ten_Laptop.split("/")
    tinh_nang = tinh_nang_Laptop.split("\n")
    
    ts_Man_Hinh_LOC= loc_Man_Hinh(tinh_nang[0])
    ts_CPU_LOC = loc_CPU(tinh_nang[1])
    ts_RAM_LOC = loc_RAM(tinh_nang[2])
    ts_O_Cung= tinh_nang[3][7:]
    if "Đồ họa" in tinh_nang[4]:
        ts_Card_Do_Hoa = tinh_nang[4][7:]
        ts_HDH = tinh_nang[5][13:]
        trong_Luong = tinh_nang[6][12:]
        xuat_Xu = tinh_nang[8][8:]
    else:
        ts_Card_Do_Hoa = ""
        ts_HDH = tinh_nang[4][13:]
        trong_Luong = tinh_nang[5][12:]
        xuat_Xu = tinh_nang[7][8:]
    noi_Ban ="FPT"
    ts_Laptop_LOC = [ten[0],gia_Laptop, ts_Man_Hinh_LOC, ts_CPU_LOC, ts_RAM_LOC,ts_O_Cung,
                     ts_Card_Do_Hoa,ts_HDH,trong_Luong,xuat_Xu,noi_Ban]
    return ts_Laptop_LOC


driver = webdriver.Chrome("C:/webdrivers/chromedriver.exe")
driver.get("https://fptshop.com.vn/may-tinh-xach-tay")
print("Done open browser")

try:
    for i in range(50):
        button_xem_them = driver.find_element(By.XPATH, "/html/body/div[2]/main/div/div[3]/div[2]/div[3]/div/div[3]/a")
        button_xem_them.click()
        sleep(2)
except:
    print("Done_Load")


computer = driver.find_elements(By.CLASS_NAME,"cdt-product__name")
link_San_Pham = [i.get_attribute("href") for i in computer]
print("Số lương máy có thể lấy:",len(link_San_Pham))


ds_LapTop_Add_Duoc = []
ds_LapTop_Add_Khong_Duoc =[]
count  =0

ds_LapTop_Add_Duoc = []
ds_LapTop_Add_Khong_Duoc =[]
count  =0
for i in link_San_Pham:
    try:
        driver.get(i)
        sleep(3)
        tinh_nang_LapTop = driver.find_element(By.CLASS_NAME, "st-pd-table").text
        ten_LapTop = driver.find_element(By.CLASS_NAME, "st-name").text
        gia_Laptop = driver.find_element(By.CLASS_NAME,"st-price-main").text.replace("₫","")
        ts_Laptop = lay_Tinh_Nang_Laptop(tinh_nang_LapTop,ten_LapTop, gia_Laptop)
        ds_LapTop_Add_Duoc.append(ts_Laptop)
    except:
        ds_LapTop_Add_Khong_Duoc.append(i)
        count+=1
        print("lỗi:",count)
        continue
    sleep(2)

print("Số lương máy không lấy được:",len(ds_LapTop_Add_Khong_Duoc))

#Phương án 1
with open("thong_Tin_Laptop_FPT.csv", "w", encoding="utf-8") as laptop:
        headers = ['TenLaptop',"GiaLaptop",'inch','DoPhanGiai','LoaiManHinh',
                   'KhacMH','HangCPU', 'DongCPU',
                  'DoiCPU','DungLuongRAM','LoaiRAM','BusRAM', 'OCung', 
                   'CardDoHoa','HDH','TrongLuong', 'XuatXu','NoiMua']
        writer = csv.writer(laptop, delimiter=",")
        writer.writerow(headers)
        for i in ds_LapTop_Add_Duoc:
            writer.writerow([i[0],i[1],i[2][0],i[2][1],i[2][2],",".join(i[2][3]),i[3][0],
                            i[3][1],i[3][2],i[4][0],i[4][1],i[4][2],i[5],
                            i[6],i[7],i[8],i[9],i[10]])
print("WRITE TO FILE")

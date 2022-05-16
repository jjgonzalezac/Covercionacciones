##INSTALACION DE SELENIUM, EL WEBDRIVER Y TKINTER

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import tkinter as tk
import tkinter as GUI
from tkinter import ttk,Entry,Button,Label,Tk,Text,StringVar,Frame, messagebox
from tkinter.messagebox import showinfo
from tkinter import *
import time 
import sys
from datetime import datetime,date


###---------FUNCTION WEBSCRAPING--------#####

def webscraping():
    global driver
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome('chromedriver', chrome_options=options)

    accion = str(accion_a_buscar.get())
    valor = str(valor_a_convertir.get())
    today = datetime.now() 
    fecha = today.strftime('%d/%m/%Y-%H:%M')
    accion_valor = ''

    #driver = webdriver.Chrome() 
    driver.get("https://finance.yahoo.com/")
    time.sleep(5)
    buscador = driver.find_element_by_xpath("//*[@id='yfin-usr-qry']")
    buscador.send_keys(accion)
    time.sleep(5)
    busqueda = driver.find_element_by_xpath("//*[@id='header-desktop-search-button']")
    busqueda.click()
    time.sleep(5)

    try:
        accion_valor = driver.find_element_by_xpath("//*[@id='quote-header-info']/div[3]/div[1]/div[1]/fin-streamer[1]")
        time.sleep(1)
        accion_valor = accion_valor.get_attribute('value')
        print(f'La acción de {accion} cuesta: $ {accion_valor}')
        usd = round((float(valor)/float(accion_valor)),3)
        print (f'El precio de la conversion es de ${usd} en la accion {accion}')
        resumen = str(fecha)+","+str(accion)+","+str(accion_valor)+","+str(valor)+","+str(usd)+"\n"
        desplegado_ventana = 'El costo de la accion es de $'+str(accion_valor)+'. La conversion a la accion '+str(accion)+ ' es de '+str(usd)+' de accion'
        driver.quit()
        messagebox.showinfo(title='RESULTDO', message=desplegado_ventana)
    
    except NoSuchElementException:
        accion_valor = driver.find_element_by_name('p')
        print(f'La acción {accion} no esta en el mercado.')
        messagebox.showinfo(title='RESULTDO', message='NO EXISTE')
        driver.quit()
        resumen = str(fecha)+","+str(accion)+','+'NO EXISTE'+"\n"
    
    historial.write(resumen)
    driver.quit()
    ###-------END FUNCTION WEBSCRAPING--------#####    



def validar_texto(accion_a_buscar):
    if len(accion_a_buscar)>0:
        return True
    return accion_a_buscar.isalnum()


def validar_numeros(valor_a_convertir):
    return valor_a_convertir.isdigit()
#-------------------------------

def desplegar_resultado_ventana():
    resultado_ventana = Tk.TopLevel()
    resultado_ventana.title("Resultado")
    boton_cerrar = ttk.Button(resultado_ventana,text="Cerrar",command=resultado_ventana.destroy)

#--------MAIN--------------------
driver = None
historial = open('historial_de_conversion.csv','w')
titulo_archivo = "Fecha,Acción,Precio de la acción,$ a Convertir,Resutado de la conversion,"+"\n"
historial.write(titulo_archivo)
ventana_principal = Tk()
ventana_principal.title('CONVERSION DE ACCIONES')
miframe = Frame(ventana_principal)
miframe.grid()


Label(miframe, text="Accion a buscar: ", fg="gray", font=("Poppins",12)).grid(row=0,column=0,sticky="w",padx=5,pady=0)
Label(miframe, text="Valor a convertir: ", fg="gray", font=("Poppins",12)).grid(row=2,column=0,sticky="w",padx=5,pady=1)

accion_a_buscar = StringVar()
accion_a_buscar_entrada = Entry(miframe,textvariable=accion_a_buscar, font=("Poppins",16),validate="key")#,validatecommand=(validar_texto,'%S', '%P'))#,command=activar_boton)
accion_a_buscar_entrada.grid(row=1,column=0,sticky="nsew",padx=10,pady=1)

valor_a_convertir = DoubleVar()
valor_a_convertir_entrada = Entry(miframe,textvariable=valor_a_convertir, font=("Poppins",16),validate="key",validatecommand=(validar_numeros,'%S','%P'))
valor_a_convertir_entrada.grid(row=3,column=0,sticky="nsew",padx=10,pady=1)

convertir_enviar = Button(miframe,text="Iniciar la conversion",fg="black",font=("Poppins,10"),command=webscraping)
convertir_enviar.grid(row=4,column=0,padx=5,pady=10)


ventana_principal.mainloop()

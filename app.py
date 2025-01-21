from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from datetime import datetime
import pandas as pd  
import time
import os 

cnpj = input('Digite o CNPJ da empresa: ')

nome_planilha = 'planilha_robo_iss.xlsx'
desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
print(f"Caminho da área de trabalho: {desktop_path}")

caminho_planilha = os.path.join(desktop_path, nome_planilha)
def configurar_driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")  
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def get_previos_month_and_year():
    today = datetime.today()
    if today.month ==  1:
        previous_month = 12
        year = today.year - 1
    else:
        previous_month = today.month - 1
        year = today.year
    return previous_month,year

mesANO = get_previos_month_and_year()
mes = mesANO[0]
ano = str(mesANO[1])


def acessar_site(url):
    driver = configurar_driver()
    #aqio
    try:
        driver.get(url)
        print(f"Acessando o site: {url}")

        wait = WebDriverWait(driver, 10)
        click_botao_login = wait.until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="login"]/div[1]/div/a[1]'))
        )
        click_botao_login.click()
        print("Cliquei em 'fazer login'")

        inserir_cpf = wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="username"]')))
        inserir_cpf.send_keys("389.256.643-72")
        time.sleep(2)

        inserir_senha = driver.find_element(By.XPATH, '//*[@id="password"]')
        inserir_senha.send_keys("Fiscal@2021")
        time.sleep(2)

        clicar_login = driver.find_element(By.XPATH, '//*[@id="botao-entrar"]')
        clicar_login.click()
        print("Login realizado com sucesso!")
        time.sleep(5)

        #login
        #inscriçao
        clicar_Cnpj = driver.find_element(By.XPATH, '//*[@id="alteraInscricaoForm:tipoPesquisa"]/tbody/tr/td[2]/label')
        actions = ActionChains(driver)
        actions.move_to_element(clicar_Cnpj).click().perform()
        print("cliquei no cnpj")
        time.sleep(2) 
        dados = pd.read_excel(caminho_planilha)
        print(f"Dados carregados:\n{dados}")

        campo_cnpj = driver.find_element(By.XPATH, '//*[@id="alteraInscricaoForm:cpfPesquisa"]')
        campo_cnpj.clear()
        campo_cnpj.send_keys(cnpj)
        time.sleep(2)

        clicar_pesquisar = driver.find_element(By.XPATH, '//*[@id="alteraInscricaoForm:btnPesquisar"]')
        clicar_pesquisar.click()
        print("cliquei em pesquisar")
        time.sleep(2)

        clicar_empresa = driver.find_element(By.XPATH, '//*[@id="alteraInscricaoForm:empresaDataTable:0:linkInscricao"]')
        clicar_empresa.click()
        print("cliquei na empresa")
        time.sleep(2)
        #inscriçao 

        #colocar a data da escrituraçao
        clicar_escrituracao = driver.find_element(By.XPATH, '//*[@id="navbar"]/ul/li[6]/a')
        clicar_escrituracao.click()
        time.sleep(2)

        clicar_escrituracao2 = driver.find_element(By.XPATH, '//*[@id="formMenuTopo:menuEscrituracao:j_id78"]')
        clicar_escrituracao2.click()
        time.sleep(2) 

        clicar_data =  driver.find_element(By.XPATH,'//*[@id="manterEscrituracaoForm:dataInicialHeader"]/label/div' ) 
        clicar_data.click()
        time.sleep(2)

        clicar_mes = driver.find_element(By.XPATH, f'//*[@id="manterEscrituracaoForm:dataInicialDateEditorLayoutM{mes - 1}"]')
        clicar_mes.click()
        time.sleep(2)

        lista_tabela_ano = driver.find_elements(By.XPATH, '//*[@id="manterEscrituracaoForm:dataInicialDateEditorLayout"]/tbody/tr/td/div')
        for i in lista_tabela_ano:
            if i.text == ano:
                i.click()
        time.sleep(1)

        clicar_ok = driver.find_element(By.XPATH, '//*[@id="manterEscrituracaoForm:dataInicialDateEditorButtonOk"]')
        clicar_ok.click()
        time.sleep(1)

        clicar_data2 = driver.find_element(By.XPATH, '//*[@id="manterEscrituracaoForm:dataFinalHeader"]/label/div')
        clicar_data2.click()
        time.sleep(1)

        clicar_mes2 = driver.find_element(By.XPATH, f'//*[@id="manterEscrituracaoForm:dataFinalDateEditorLayoutM{mes - 1}"]')
        clicar_mes2.click()
        time.sleep(1)

        lista_tabela_ano2 = driver.find_elements(By.XPATH, '//*[@id="manterEscrituracaoForm:dataFinalDateEditorLayout"]/tbody/tr/td/div')
        for i in lista_tabela_ano2:
            if i.text == ano:
                i.click()
        time.sleep(1)

        clicar_ok = driver.find_element(By.XPATH, '//*[@id="manterEscrituracaoForm:dataFinalDateEditorButtonOk"]')
        clicar_ok.click()
        time.sleep(2)

        clicar_consultar = driver.find_element(By.XPATH, '//*[@id="manterEscrituracaoForm:btnConsultar"]')
        clicar_consultar.click()
        time.sleep(2)

        clicar_escriturar = driver.find_element(By.XPATH, '//*[@id="manterEscrituracaoForm:dataTable:0:escriturar"]')
        clicar_escriturar.click()
        time.sleep(10)
        #colocar a data da escrituraçao

        #indo para colocar dado para escriturar
        clicar_tomados = driver.find_element(By.XPATH, '//*[@id="aba_tomados_lbl"]')
        clicar_tomados.click()
        time.sleep(2)

        clicar_digitardoc = driver.find_element(By.XPATH, '//*[@id="servico_tomado_form:seamj_id836"]')
        clicar_digitardoc.click()
        time.sleep(2)
        #indo para colocar dado para escriturar

        #escriturando
        clicar_cnpj_prestador = driver.find_element(By.XPATH, '//*[@id="digitarDocumentoForm:tipoPesquisaTomadorRb"]/tbody/tr/td[2]/label')
        actions = ActionChains(driver)
        actions.move_to_element(clicar_cnpj_prestador).click().perform()
        time.sleep(1)

        clicar_colocar_cnpj = driver.find_element(By.XPATH, '//*[@id="digitarDocumentoForm:cpfPesquisaTomador"]')
        clicar_colocar_cnpj.click()
        for index, row in dados.iterrows():
            driver.find_element(By.XPATH, '//*[@id="digitarDocumentoForm:cpfPesquisaTomador"]').send_keys(row['CNPJ'])
            time.sleep(1)
            clicar_colocar_cnpj.send_keys(Keys.ENTER)
        time.sleep(2) 
       
        clicar_servico = driver.find_element(By.XPATH, '//*[@id="digitarDocumentoForm:abaServico_lbl"]')
        clicar_servico.click()
        time.sleep(2)

        clicar_select = driver.find_element(By.XPATH, '//*[@id="digitarDocumentoForm:tipoDocumentoDigitado"]')
        clicar_select.click()
        time.sleep(2)
        for i in range(1):
            clicar_select.send_keys(Keys.ARROW_DOWN)
            time.sleep(2)
            clicar_select.send_keys(Keys.ENTER)
            time.sleep(2)

        clicar_numero = driver.find_element(By.XPATH, '//*[@id="digitarDocumentoForm:numeroDocumentoDigitado"]')
        clicar_numero.click()
        driver.find_element(By.XPATH, '//*[@id="digitarDocumentoForm:numeroDocumentoDigitado"]').send_keys(row['Nº DOCUMENTO'])
        time.sleep(1)

        clicar_serie = driver.find_element(By.XPATH, '//*[@id="digitarDocumentoForm:serieDocumentoDigitado"]')
        clicar_serie.send_keys('E')

        dados['DATA DOCUMENTO'] = pd.to_datetime(dados['DATA DOCUMENTO'], errors='coerce').dt.strftime('%d/%m/%Y')
        if dados['DATA DOCUMENTO'].isnull().any():
            print("Há valores inválidos na coluna 'DATA DOCUMENTO'. Por favor, revise a planilha.")
        else:
            for index,row in dados.iterrows():
                dataDoc = driver.find_element(By.XPATH, '//*[@id="digitarDocumentoForm:dataEmissaoInputDate"]')
                dataDoc.clear()
                dataDoc.send_keys(row['DATA DOCUMENTO'])
                time.sleep(2)

        clicar_situacao = driver.find_element(By.XPATH, '//*[@id="digitarDocumentoForm:statusNfse"]')
        clicar_situacao.click()
        time.sleep(2)
        for i in range(1):
            clicar_situacao.send_keys(Keys.ARROW_DOWN)
            time.sleep(2)
        clicar_situacao.send_keys(Keys.ENTER)
        time.sleep(2)

        clicar_pesquisarCnae = driver.find_element(By.XPATH, '//*[@id="digitarDocumentoForm:idLinkPesquisarCnae"]')
        clicar_pesquisarCnae.click()
        time.sleep(2)

        codigoCnae = driver.find_element(By.XPATH, '//*[@id="digitarDocumentoForm:idFormularioPesquisaCnae:idCnaePesquisa"]')
        codigoCnae.click()
        driver.find_element(By.XPATH, '//*[@id="digitarDocumentoForm:idFormularioPesquisaCnae:idCnaePesquisa"]').send_keys(row['CODIGO CNAE'])
        time.sleep(2)
        
        fecharCnae = driver.find_element(By.XPATH, '//*[@id="digitarDocumentoForm:idFormularioPesquisaCnae:idPesquisar"]')
        fecharCnae.click()
        time.sleep(1000)

        clicar_opçaoCnae = driver.find_element(By.XPATH, '//*[@id="digitarDocumentoForm:idFormularioPesquisaCnae:idDatatableListaCnae:0:j_id451"]')
        clicar_opçaoCnae.click()
        time.sleep(10000)



    except Exception as e:
        print(f"Erro ao acessar o site: {e}")



acessar_site("https://iss.fortaleza.ce.gov.br/grpfor/login.seam?cid=33110")

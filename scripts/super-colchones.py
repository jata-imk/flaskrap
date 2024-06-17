import os
import sys

# Agregar el directorio principal del proyecto a sys.path para que se puedan importar los módulos de la aplicación
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app
from app.main.services.product_service import ProductService
from app.main.services.inventory_service import InventoryService
from app.utils.string_formatter import clean_number

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from urllib.parse import urlparse, parse_qs, urlencode

# import time
import uuid

app = create_app()
app.app_context().push()

class SuperColchonesWebScrapper:
    urlBase = "https://www.supercolchones.com.mx/"
    endpointCatalogSearchResults = "catalogsearch/result/index/"
    
    def __init__(self, debug = False):
        options = None
        
        if (debug is False):
            print('Running in headless mode...\n\n')
            options = Options()
            options.add_argument("--headless=new")
            options.add_experimental_option("excludeSwitches", ["enable-logging"])

        driver = webdriver.Chrome(options)
        driver.get(self.urlBase)
        driver.implicitly_wait(5)

        self.driver = driver

    def selectPageWrapper(self):
        pageWrapper = None

        pageWrapper = self.driver.find_element(by=By.ID, value='html-body')
        pageWrapper = pageWrapper.find_element(by=By.CSS_SELECTOR, value='* > div.page-wrapper')
        
        return pageWrapper
    
    def selectHeader(self):
        pageWrapper = self.selectPageWrapper()
        pageHeader = pageWrapper.find_element(by=By.CSS_SELECTOR, value='header.page-header')

        return pageHeader
    
    def selectMainContent(self):
        pageWrapper = self.selectPageWrapper()
        mainContent = pageWrapper.find_element(by=By.ID, value='maincontent')

        return mainContent

    def selectSearchBox(self):
        pageHeader = self.selectHeader()

        search_box = pageHeader.find_element(by=By.CSS_SELECTOR, value='.header.content .block-content form input#search')
        
        return search_box
    
    def selectFilterSection(self):
        mainContent = self.selectMainContent()
        
        filterSection = mainContent.find_element(by=By.CSS_SELECTOR, value='* > .columns > .sidebar.sidebar-main')

        return filterSection
    
    def selectResultsContainer(self):
        try:
            mainContent = self.selectMainContent()

            resultsContainer = mainContent.find_element(by=By.CSS_SELECTOR, value='* > .columns > .column.main')
            resultsContainer = resultsContainer.find_element(by=By.CSS_SELECTOR, value='* > .search.results > .products.wrapper')

            return resultsContainer
        except NoSuchElementException:
            return None
        
filters = {
    'cat' : {
        'title' : 'Categoría',
        'value' : 'Colchones'
    },
    'manufacturer' : {
        'title': 'Marca',
        'value': [5448] # Spring air
    },
    'tipo' : {
        'title': 'Tipo',
        'value': 'Resorte'
    },
    'size' : {
        'title': 'Tamaño',
        'value': 'Individual'
    },
    'confort' : {
        'title': 'Nivel de Confort',
        'value': ''
    },
    'juego_box' : {
        'title': 'Juego de box',
        'value': '', # Valores Posibles -> Si
    },
}
    
superColchonesWeb = SuperColchonesWebScrapper() 

# Ingresamos a la pagina principal y el flujo a seguir sera el siguiente
# 1. Ingresar a la pagina principal y hacer la búsqueda de la palabra clave
search_box = superColchonesWeb.selectSearchBox()
search_box.click()

search_box.send_keys('Colchon Spring Hair')
search_box.submit()

# 2. Cargar la lista de coincidencias y aplicar los filtros pero no haciendo
#    click si no recorriendo los elementos de los filtros y obteniendo sus ID
#    para luego formar una URL y posteriormente cargar esa dirección
filterSection = superColchonesWeb.selectFilterSection()
filterOptionsContainer = filterSection.find_element(by=By.CSS_SELECTOR, value='* > #layered-filter-block .filter-content .filter-options')
filterOptions = filterOptionsContainer.find_elements(by=By.CSS_SELECTOR, value='* > .filter-options-item')

# Recorremos los filtros para obtener los ID de cada uno
# filterOptions contiene un listado de DIV los cuales cada uno tiene dos nodos
# el primero es el titulo y el segundo el contenido

filterParameters = {
    'q' : ['Colchon Spring Hair']
}

# brandsLists se ocupa para guardar un arreglo de objetos que contienen el nombre de la marca y su ID
# esto sera util mas adelante cuando vayamos a guardar los productos
brandsList = []

for filterOption in filterOptions:
    title = filterOption.find_element(by=By.CSS_SELECTOR, value='* > .filter-options-title')
    itemsList = filterOption.find_element(by=By.CSS_SELECTOR, value='* > .filter-options-content ol.items')
    items = itemsList.find_elements(by=By.CSS_SELECTOR, value='* > .item')
    
    for item in items:
        # select the link inside
        itemAnchor = item.find_element(by=By.CSS_SELECTOR, value='* > a')
        itemAnchorText = superColchonesWeb.driver.execute_script("return arguments[0].childNodes[0].textContent;", itemAnchor)
        itemAnchorText = itemAnchorText.strip()

        # get URL (itemAnchor) parameters
        itemAnchorHref = itemAnchor.get_attribute('href')
        itemAnchorHrefParsed = urlparse(itemAnchorHref)
        itemAnchorHrefParams = parse_qs(itemAnchorHrefParsed.query)

        # filter params different than q
        itemAnchorHrefParams = {k: v[0] for k, v in itemAnchorHrefParams.items() if k != 'q'}

        # Obtiene la llave correspondiente del diccionario itemAnchorHrefParams
        itemAnchorHrefParamsKey = next(iter(itemAnchorHrefParams.keys()))
        itemAnchorHrefParamsValue = next(iter(itemAnchorHrefParams.values()))

        # Obtiene el valor correspondiente del diccionario filters usando la llave obtenida
        filterValue = filters.get(itemAnchorHrefParamsKey)

        if title.text.strip() == 'Marca':
            if (len(filters['manufacturer']['value']) == 0 or int(itemAnchorHrefParamsValue) in filters['manufacturer']['value']):
                brandsList.append({'name': itemAnchorText, 'id': itemAnchorHrefParamsValue})

        if (filterValue['value'] != '' and filterValue['value'] == itemAnchorText):
            filterParameters[itemAnchorHrefParamsKey] = [itemAnchorHrefParamsValue]
            
urlcatalogSearchResults = superColchonesWeb.urlBase + superColchonesWeb.endpointCatalogSearchResults
urlcatalogSearchResults = urlcatalogSearchResults + "?" + urlencode(filterParameters, doseq=True)

scraped_products = [];
for brand in brandsList:
    filterParameters['manufacturer'] = [brand['id']]
    urlcatalogSearchResults = superColchonesWeb.urlBase + superColchonesWeb.endpointCatalogSearchResults
    urlcatalogSearchResults = urlcatalogSearchResults + "?" + urlencode(filterParameters, doseq=True)

    superColchonesWeb.driver.get(urlcatalogSearchResults)

    # 3. Iterar los resultados filtrados y obtener los precios Desde de todos los colchones
    #    ademas de también guardar su modelo y su marca
    #    igualmente se selecciona un modelo en particular y se visita su pagina y se guardan todos sus precios
    resultsContainer = superColchonesWeb.selectResultsContainer()

    if resultsContainer is None:
        continue

    productsList = resultsContainer.find_elements(by=By.CSS_SELECTOR, value='* > ol.product-items > li.product-item')

    for productItem in productsList:
        productItemInfo = productItem.find_element(by=By.CSS_SELECTOR, value='* > .product-item-info')
        productAnchor = productItemInfo.find_element(by=By.CSS_SELECTOR, value='* > a')
        productAnchorHref = productAnchor.get_attribute('href')

        productItemName = productItemInfo.find_element(by=By.CSS_SELECTOR, value='.product-item-name > a')

        productItemPrice = None
        try:
            productItemPrice = productItemInfo.find_element(by=By.CSS_SELECTOR, value='.price-final_price > span.normal-price .price')
        except NoSuchElementException:
            print("No se encontró el elemento span.normal-price, tratando de buscar span.special-price")
            productItemPrice = productItemInfo.find_element(by=By.CSS_SELECTOR, value='.price-final_price > span.special-price .price')
        
        if productItemPrice is None:
            print("No se encontró el elemento span.normal-price ni span.special-price, no se agregara el historico del producto, continuando con el siguiente.")
            continue

        productItemFormToCart = productItemInfo.find_element(by=By.CSS_SELECTOR, value='* > .product-item-details .product-item-actions > .actions-primary > form')
        productItemSku = productItemFormToCart.get_attribute('data-product-sku')

        objectProduct = {
            'name': productItemName.text,
            'categories': ['Muebles', 'Recámaras', 'Camas y bases'],
            'brand': brand['name'],
            'vendor': 'Super Colchones',
            'price':  clean_number(productItemPrice.text),
            'sku': 'alz-' + str(uuid.uuid4()),
            'vendor_sku': productItemSku
        }
        scraped_products.append(objectProduct)

    for product_data in scraped_products:
        # Suponiendo que ProductService.get_or_create_product maneja la lógica de productos
        product = ProductService.get_or_create_product(product_data)
        product_inventory  = ProductService.get_or_create_product_inventory(product_data)
        
        # Registrar transacción de entrada de inventario
        InventoryService.log_io_transaction(
            inventory_id=product_inventory.id,
            io_type='PRICE_UPDATE',
            quantity=0,  # Ejemplo: 1 unidad
            price=product_data['price'],
        )

# wait on this screen, not close the browser
# time.sleep(500)

superColchonesWeb.driver.quit() # close the browser
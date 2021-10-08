#!/usr/bin/env python
# coding: utf-8

# In[22]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[23]:


path = r"C:\Users\SoyTh\Downloads\synergy_logistics_database.csv"


# In[24]:


data = pd.read_csv(path, index_col = "register_id")
data


# In[4]:


#Vemos que tipos de datos tenemos y si contamos con datos nulos.
data.info()


# In[5]:


#Ver el número de importaciones y exportaciones.
data["direction"].value_counts()


# In[6]:


#Nos fijamos en los diferentes paises con los que contamos en nuestra base de datos y cómo se dividen.
print("Hay ",data.origin.nunique(),"paises de origenes.")
print("Y son ",data.destination.nunique(), "los paises de destino.")


# In[7]:


#Consultamos durante cuantos años se ha estado operando, así como la cantidad de operaciones por año.
data["year"].value_counts()


# In[8]:


#Nos fijamos en los números de transportes con los que contamos y la frecuencia con la que se utilizan.
data["transport_mode"].value_counts()


# In[9]:


#Número de compañías diferentes con las que se tiene relación
data["company_name"].nunique()


# In[10]:


#Tipos de productos diferentes.
data["product"].nunique()


# In[11]:


#Vemos cómo se comporta nuestra filas de valor.
data["total_value"].describe()


# In[4]:


#Pasamos a tipo dato nuestra fila de fecha.
data["date"]= pd.to_datetime(data["date"])


# In[5]:


#Graficamos el total del valor por año y vemos como va variando.
get_ipython().run_line_magic('matplotlib', 'inline')
plt.figure(figsize = (15,8))
sns.lineplot(x = data["date"], y = data["total_value"])


# In[25]:


#Hacemos dos tablas difentes para ver por separado nuestras importaciones y exportaciones.
filtro_exportaciones = data["direction"] == "Exports"
filtro_importaciones = data["direction"] == "Imports"
display(data[filtro_exportaciones])
display(data[filtro_importaciones])


# In[26]:


#Nos fijamos en la cantidad de exportaciones que realiza cada país.
data[filtro_exportaciones]["origin"].value_counts().head(10)


# In[27]:


#Nos fijamos en la cantidad de importaciones que realiza cada país.
data[filtro_importaciones]["origin"].value_counts().head(10)


# Una vez hecho este pequeño análisis vamos a resolver el primer punto, calcular las 10 rutas más demandadas de importaciones y exportaciones.

# In[28]:


#Para esto creamos un data frame con los datos de nuestro interés.
df_reducido = data[['direction', 'origin', 'destination', 'transport_mode', 'total_value']]


# In[29]:


rutas_imports = df_reducido[df_reducido["direction"] == "Imports"]
rutas_exports = df_reducido[df_reducido["direction"] == "Exports"]
display(rutas_imports)
display(rutas_exports)


# In[33]:


#Agrupamos por estas categorias y obtenemos la frecuencia.
rutas_unicas_imports = rutas_imports.groupby(['direction', 'origin', 'destination', 'transport_mode']).count()
display(rutas_unicas_imports)
rutas_unicas_exports = rutas_exports.groupby(['direction', 'origin', 'destination', 'transport_mode']).count()
display(rutas_unicas_exports)


# In[34]:


rutas_unicas_imports.rename(columns={'total_value' : 'count'}, inplace = True)
rutas_unicas_imports
rutas_unicas_exports.rename(columns={'total_value' : 'count'}, inplace = True)
rutas_unicas_exports


# In[35]:


#Ordenamos nuestros DF en función a la mayor cantidad de frecuencia de cada ruta.
rutas_unicas_imports  = rutas_unicas_imports.sort_values(by="count", ascending = False)
rutas_unicas_exports = rutas_unicas_exports.sort_values(by="count", ascending = False)


# In[36]:


#Imprimimos los primero 10 datos de nuestro DF.
display(rutas_unicas_exports.head(10))
display(rutas_unicas_imports.head(10))


# Ahora nos va interesar obtener en dos diferentes Data Frames las importaciones y exportaciones del Data Frame de rutas, para 
# De esa forma saber las rutas más frecuentes de importación y exportación.

# In[37]:


rutas_unicas_exports['nombre'] = rutas_unicas_exports.index.to_list()
rutas_unicas_imports['nombre'] = rutas_unicas_imports.index.to_list()


# In[39]:


#Definimos una función para renombrar el formato de nuestra última columna de nuestro DF anterior.
def nombre_nuevo(lista):
    nombre = lista[1]+" - "+lista[2]+" , "+ lista[3]
    return nombre


# In[40]:


#Aplicamos la función a los dos DF de nuestras rutas más demandadas.
rutas_unicas_exports['nombre'] = rutas_unicas_exports['nombre'].apply(nombre_nuevo)
rutas_unicas_imports['nombre'] = rutas_unicas_imports['nombre'].apply(nombre_nuevo)


# In[41]:


#Imprimimos nuestras últimas tablas
display(rutas_unicas_exports.head(10))
display(rutas_unicas_imports.head(10))


# In[42]:


#Por lo que nuestras principales 10 rutas de importación y exportación están dadas por:
top_10_rutas_importacion = rutas_unicas_imports[["nombre", "count"]]
top_10_rutas_importacion.rename(columns={'count' : 'frecuencia', "nombre":"ruta"}, inplace = True)
top_10_rutas_importacion.reset_index(inplace = True)
top_10_rutas_importacion = top_10_rutas_importacion[["ruta", "frecuencia"]].head(10)

top_10_rutas_exportacion = rutas_unicas_exports[["nombre", "count"]]
top_10_rutas_exportacion.rename(columns={'count' : 'frecuencia', "nombre":"ruta"}, inplace = True)
top_10_rutas_exportacion.reset_index(inplace = True)
top_10_rutas_exportacion = top_10_rutas_exportacion[["ruta", "frecuencia"]].head(10)


# In[43]:


display(top_10_rutas_exportacion)
display(top_10_rutas_importacion)


# In[30]:


sns.set(rc={"figure.figsize": (18, 6)}) 
sns.barplot(data=rutas_unicas_imports.head(10), x='nombre', y='count')


# Ahora obtendremos el segundo punto del assessment 

# In[44]:


#Para esto consideraremos solamente las filas de nuestros interés.
#Entonces de nuestra data nos traemos la columna de transport_mode y total_value
transportes = data[["transport_mode", "total_value"]]
transportes


# In[45]:


#Agrupado por transporte y sumamos el total_value correpondiente a cada uno.
top_transportes = transportes.groupby("transport_mode")["total_value"].sum()


# In[46]:


#Ordenamos nuestros valores.
top_transportes.sort_values(axis=0, ascending=False, inplace = True)


# In[47]:


#Acomodamos nuestro DF de medios de transporte.
top_transportes = top_transportes.reset_index()


# In[49]:


top_transportes


# In[48]:


#Graficamos nuestra ganancia por transporte
get_ipython().run_line_magic('matplotlib', 'inline')
sns.barplot(x = top_transportes["transport_mode"], y = top_transportes["total_value"])
plt.ylabel('Medios de transportes')
plt.xlabel('Cantidad de Valor')
plt.title('Tranportes más usados')
plt.show()


# In[38]:


#Por lo que nuestros 3 tranportes más importantes son
los_3_transportes_mas_importantes = top_transportes.head(3)


# In[39]:


#Graficamos los 3 más importantes
get_ipython().run_line_magic('matplotlib', 'inline')
sns.barplot(x = los_3_transportes_mas_importantes["transport_mode"], y = los_3_transportes_mas_importantes["total_value"])
plt.xlabel('Cantidad de Valor')
plt.title('Tranportes más usados')
plt.show()


# Notemos que hicimos lo anterior contando importaciones y exportaciones, pero el problema nos pide que nos fijemos por seperado, es decir, los medios de transporte más importantes para importaciones y exportaciones, por lo que procedemos a hacer todo lo anterior por separado.

# In[40]:


transportes_exp = data[["transport_mode", "total_value"]][data["direction"] == "Exports"]
transportes_imp = data[["transport_mode", "total_value"]][data["direction"] == "Imports"]
top_transportes_exp= transportes_exp.groupby("transport_mode")["total_value"].sum()
top_transportes_imp = transportes_imp.groupby("transport_mode")["total_value"].sum()


# In[41]:


top_transportes_exp.sort_values(axis=0, ascending=False, inplace = True)
top_transportes_imp.sort_values(axis=0, ascending=False, inplace = True)

top_transportes_exp = top_transportes_exp.reset_index()
top_transportes_imp = top_transportes_imp.reset_index()


# In[42]:


los_3_transportes_mas_importantes_exp = top_transportes_exp.head(3)
los_3_transportes_mas_importantes_imp = top_transportes_imp.head(3)


# Ahora gráficamos 

# In[43]:


#Graficamos los 3 tranportes más importantes para exportaciones
get_ipython().run_line_magic('matplotlib', 'inline')
sns.barplot(x = los_3_transportes_mas_importantes_exp["transport_mode"], y = los_3_transportes_mas_importantes_exp["total_value"])
plt.xlabel('Cantidad de Valor')
plt.title('Tranportes más usados en exportaciones')
plt.show()


# In[44]:


#Graficamos los 3 tranportes más importantes para exportaciones
get_ipython().run_line_magic('matplotlib', 'inline')
sns.barplot(x = los_3_transportes_mas_importantes_imp["transport_mode"], y = los_3_transportes_mas_importantes_imp["total_value"])
plt.xlabel('Cantidad de Valor')
plt.title('Tranportes más usados en importaciones')
plt.show()

Por último calcularemos el último punto.
# In[50]:


#Hagamos un data frame con los datos de interes, que en este caso son los paises y el valor
paises = data[["origin", "total_value"]]


# In[51]:


#Agrupamos por paises y contamos el total_value, y tembién ordenamos por su valor y de forma descendente
paises_mas_importantes = paises.groupby("origin").sum().sort_values("total_value", ascending=False)


# In[52]:


paises_mas_importantes.reset_index(inplace = True)
paises_mas_importantes.rename(columns = {"origin": "país", "total_value":"valor"}, inplace = True)


# In[53]:


valor_total = sum(paises_mas_importantes["valor"])


# In[54]:


paises_mas_importantes["influencia"] = paises_mas_importantes["valor"] / valor_total


# In[55]:


#Graficamos la influencia de cada país en su valor
get_ipython().run_line_magic('matplotlib', 'inline')
plt.figure(figsize=(15, 6))
sns.barplot(x = paises_mas_importantes["país"], y = paises_mas_importantes["valor"])
plt.xlabel('Cantidad de Valor')
plt.title('País')
plt.show()


# In[56]:


paises_mas_importantes["influencia acumulada"] = 0


# In[57]:


influencia_acumulada = 0
for i in range(0, len(paises_mas_importantes)) :
    datos = paises_mas_importantes.iloc[i]
    valor = datos[2]
    influencia_acumulada += valor
    paises_mas_importantes.iloc[i]["influencia acumulada"] = influencia_acumulada


# In[63]:


#De aquí notamos que nuestros paises con el 80% de influencias son 8, de los cuales guardaremos en otro data frame
paises_con_el_80 = paises_mas_importantes.head(8)
paises_con_el_80["país"]


# In[111]:


get_ipython().run_line_magic('matplotlib', 'inline')
plt.figure(figsize=(15, 6))
sns.barplot(x = paises_con_el_80["país"], y = paises_con_el_80["valor"])
plt.xlabel('Cantidad de Valor')
plt.title('País')
plt.show()


# In[67]:


len(data["origin"].value_counts())


# In[ ]:





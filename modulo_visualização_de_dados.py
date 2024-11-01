import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

df = pd.read_csv('ecommerce_preparados.csv')
print(df.head())

df['Qtd_Vendidos'] = df['Qtd_Vendidos'].replace(to_replace=r'\+', value='', regex=True)


def converter_para_numero(texto):
    if 'mil' in texto :
        numero = int(texto.replace('+', '').replace('mil', '').strip()) * 1000
    elif 'Nenhum' in texto :
        numero = 0
    else :
        numero = int(texto)
    return numero

# Aplicação as colunas no DF
df['Qtd_vendidas_convertido'] = df['Qtd_Vendidos'].apply(converter_para_numero)

# Preencher valores NaN com zero e inferir tipos de objetos
df['Qtd_vendidas_convertido'] = df['Qtd_vendidas_convertido'].fillna(0).infer_objects(copy=False)
df['Qtd_Vendidos_Cod'] = df['Qtd_Vendidos_Cod'].fillna(0).infer_objects(copy=False)

# Completar os valores e converter para inteiro
df['Qtd_total'] = df.apply(
    lambda row: int(row['Qtd_vendidas_convertido']) if pd.notnull(row['Qtd_vendidas_convertido']) else int(row['Qtd_Vendidos_Cod']),
    axis=1)

#Grafico de Dispersão
sns.scatterplot(x='Qtd_vendidas_convertido', y='Preço', data=df)
plt.title('Preço x Quantidade total de vendas')
plt.xlabel('Quantidade total de vendas')
plt.ylabel('Preço')
plt.show()

#Heat map de Correlação
corr = df[['Qtd_vendidas_convertido','Nota','Marca_Cod']].corr()

#Renomeando as colunas apenas no gráfico
nome_novo = ['Quantidade de Vendas', 'Nota', 'Marcas']

#Mapa de correlação
sns.heatmap(corr, annot=True, cmap='coolwarm', xticklabels=nome_novo, yticklabels=nome_novo)
plt.title('Mapa de Calor de Correlação')
plt.show()

#Grafico em barra

sns.barplot(x='Qtd_vendidas_convertido', y='Gênero', data=df)
plt.title('Gênero x Quantidade total de vendas')
plt.xlabel('Quantidade total de vendas')
plt.ylabel('Gênero')
plt.show()

#Gráfico de pizza
x = df['Gênero'].value_counts().index
y = df['Gênero'].value_counts().values
plt.figure(figsize=(10,6))
plt.pie(y,labels=x,autopct='%.1f%%', startangle=90)
plt.title('Gênero x Quantidade total de vendas')
plt.show()

#Grafico de Densidade
sns.kdeplot(df['Nota'])
plt.title('Densidade da Quantidade total de Notas')
plt.xlabel('Nota')
plt.show()

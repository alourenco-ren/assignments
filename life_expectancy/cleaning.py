'''
Module docstring
'''
import pandas as pd
import click 

def clean_data(country: str):
    '''
    Performs ETL. 
    Loads data from a tsv file, then cleans and filter to only portuguese non null values 
    and finally saves to a new csv file
    '''
    #Load data
    data = pd.read_csv('life_expectancy/data/eu_life_expectancy_raw.tsv', sep="\t")
    data = data.rename(columns={'unit,sex,age,geo\\time':'info'})

    #Unpivots the date-value pair and extracts the different columns from the first
    data = data.melt(
        id_vars='info',
        var_name='year',
        value_name='value'
    )
    data[['unit', 'sex', 'age', 'region']] = data['info'].str.split(",", expand=True)
    data = data.drop('info', axis=1)

    #Cleans the numeric data and filters for portuguese values
    data['year'] = pd.to_numeric(data['year'], errors="coerce").astype("Int64")
    data['value'] = data['value'].str.replace(r"[^0-9.\-]", "", regex=True)
    data['value'] = pd.to_numeric(data['value'], errors="coerce")
    data = data.dropna(subset=['value'])
    data = data[data['region'] == country]

    #Sets final order
    data = data[['unit', 'sex', 'age', 'region', 'year', 'value']]

    #Writes result in a csv
    data.to_csv('life_expectancy/data/pt_life_expectancy.csv', index=False)

@click.command()
@click.option("--country", "-c", default="PT", help="Country to filter the results by")
def cli(country):
    clean_data(country)

if __name__ == "__main__":  # pragma: no cover
    cli()
'''
Module docstring
'''
import pandas as pd
import click

def load_data() -> pd.DataFrame:
    '''
    Loads the data and returns it in a DataFrame
    '''
    return pd.read_csv('life_expectancy/data/eu_life_expectancy_raw.tsv', sep="\t")



def clean_data(data: pd.DataFrame, country: str) -> pd.DataFrame:
    '''
    cleans and filters by {country} removing rows with null values
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

    #Cleans the numeric data and filters by {country}
    data['year'] = pd.to_numeric(data['year'], errors="coerce").astype("Int64")
    data['value'] = data['value'].str.replace(r"[^0-9.\-]", "", regex=True)
    data['value'] = pd.to_numeric(data['value'], errors="coerce")
    data = data.dropna(subset=['value'])
    if country:
        data = data[data['region'] == country]

    #Sets final order
    data = data[['unit', 'sex', 'age', 'region', 'year', 'value']]

    return data


def save_data(data: pd.DataFrame) -> None:
    '''
    Saves the DataFrame received as an argument into a csv file
    '''
    data.to_csv('life_expectancy/data/pt_life_expectancy.csv', index=False)


def main(country: str=None) -> None:
    '''
    Main function to run from terminal.
    Runs the sequence of loading, cleaning and saving the data
    '''
    data = load_data()
    data = clean_data(data, country)
    save_data(data)


@click.command()
@click.option("--country", "-c", default="PT", help="Country to filter the results by")
def cli(country: str) -> None:
    '''Deals with command line arguments'''
    main(country)


if __name__ == "__main__":  # pragma: no cover
    cli()   # pylint: disable=no-value-for-parameter

if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@transformer
def transform(data, *args, **kwargs):
   
    # Specify your transformation logic here

    # print(f"pre: missing passenger count: {data['passenger_count'].isna().sum()}")
    # data["passenger_count"].fillna(0, inplace=True)
    # print(f"post: missing passenger count: {data['passenger_count'].isna().sum()}")

    print(f"pre: missing passenger count: {data['passenger_count'].isin([0]).sum()}")
    return data[data['passenger_count'] > 0]

@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'

# IKEA Stock Checker

### Use
Execution:
`python3 ikea_stock_checker.py <product_code> <store_id1> <store_id2> ...`

Returns (example of one store):
```
[
    {
        'store_id': 168,
        'available_stock': 11,
        'in_stock_probability': 'HIGH',
        'restock_date': None,
        'forecast_1': {
            'forecast_date': '2021-04-10',
            'forecast_stock': 7
        },
        'forecast_2': {
            'forecast_date': '2021-04-10',
            'forecast_stock': 7
        },
        'forecast_3': {
            'forecast_date': '2021-04-10',
            'forecast_stock': 7
        },
        'forecast_4': {
            'forecast_date': '2021-04-10',
            'forecast_stock': 7
        }
    }
]
```

Creates a text file in same directory as script, which is updated every execution.

Dependancies:
requests==2.25.1
beautifulsoup4==4.9.3

### Fields used from XML response
restockdate
availablestock
instockprobabilitycode
forecasts

<!--
### Store format in XML response
partnumber
ismultiproduct
issoldinstore
isinstorerange
restockdate (sometimes N/A)
isvalidfornotification (sometimes N/A)
availablestock
stockavailinfocode (sometimes N/A)
instockprobabilitycode
validdate
forecasts
finditlist
-->
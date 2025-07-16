global_electricity_production_data

1 The date field is stored as a string and should be converted to a proper date/datetime type

2 The [value] column contains missing values.

3 In the product column, the entry electricity does not refer to a specific energy source (like coal or solar) but to the aggregated flow of electricity itself—representing total electricity after generation, regardless of how it was produced.
Visual explanation:
[parameter]                | [product]
Net Electricity Production | electricity → means total electricity produced (from all sources). And can be used for overall totals.

[parameter]   | [product]
Total Imports | electricity → means electricity imported from another country, not a specific fuel.


4 
| Parameter                  | Meaning                                           | Sign (assumption)     |
|----------------------------|---------------------------------------------------|-----------------------|
| Net Electricity Production | Electricity generated within the country.         | + (adds to supply)    |
| Consumption (Calculated)   | Electricity consumed domestically.                | – (draws from supply) |
| Distribution Losses        | Losses during transmission and distribution.      | – (draws from supply) |
| Total Imports              | Electricity imported from other countries.        | + (adds to supply)    |
| Total Exports              | Electricity exported to other countries.          | – (draws from supply) |
| Used for pumped storage    | Electricity used to pump water into storage.      | – (draws from supply) |



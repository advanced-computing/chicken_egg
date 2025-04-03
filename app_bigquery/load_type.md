This file will explain what type of data loading we will use for our database.

In short, it will be append load. As far as we can tell, there is no modifications made to the data columns during different updates, so there is no need for incremental load. Similarly, truncate and load will not be necessary as the data sources simply add more records, so a complete overhaul is not necessary.

If the difference in performance is small, it may be worth incorporating truncate and load as there's a chance some of the historical data is updated for the birdflu (i.e. changing outbreaks formerly with 0 chickens to a different value), but for now append will work for the purpose of our project. (Also, there is no documentation indicating the data will be updates in such a way)
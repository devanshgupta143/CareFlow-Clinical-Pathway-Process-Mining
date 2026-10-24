let
    // 1. Define Date Range based on hospital log bounds
    StartDate = #date(2025, 1, 1),
    EndDate = #date(2026, 12, 31),
    DurationDays = Duration.Days(EndDate - StartDate) + 1,
    
    // 2. Generate Date List
    DateList = List.Dates(StartDate, DurationDays, #duration(1, 0, 0, 0)),
    TableFromList = Table.FromList(DateList, Splitter.SplitByNothing(), {"Date"}, null, ExtraValues.Error),
    ChangedType = Table.TransformColumnTypes(TableFromList,{{"Date", type date}}),
    
    // 3. Extract Calendar Attributes
    InsertedYear = Table.AddColumn(ChangedType, "Year", each Date.Year([Date]), Int64.Type),
    InsertedMonth = Table.AddColumn(InsertedYear, "Month", each Date.Month([Date]), Int64.Type),
    InsertedMonthName = Table.AddColumn(InsertedMonth, "MonthName", each Date.MonthName([Date]), type text),
    InsertedQuarter = Table.AddColumn(InsertedMonthName, "Quarter", each "Q" & Text.From(Date.QuarterOfYear([Date])), type text),
    InsertedDayOfWeek = Table.AddColumn(InsertedQuarter, "DayOfWeek", each Date.DayOfWeekName([Date]), type text)
in
    InsertedDayOfWeek

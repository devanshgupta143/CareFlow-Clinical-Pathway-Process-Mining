let
    // 1. Reference existing cleaned table or load source
    Source = Csv.Document(File.Contents("mock_hospital_logs.csv"), [Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    TypedTable = Table.TransformColumnTypes(PromotedHeaders,{{"Timestamp", type datetime}}),
    
    // 2. Group by Patient to find Min (Start) and Max (End) timestamps
    GroupedRows = Table.Group(TypedTable, {"Patient_ID"}, {
        {"Admission_Start", each List.Min([Timestamp]), type datetime},
        {"Discharge_End", each List.Max([Timestamp]), type datetime}
    }),
    
    // 3. Calculate Total Lead Time in Minutes
    AddedLeadTime = Table.AddColumn(GroupedRows, "Total_Lead_Time_Mins", each Duration.TotalMinutes([Discharge_End] - [Admission_Start]), type number)
in
    AddedLeadTime

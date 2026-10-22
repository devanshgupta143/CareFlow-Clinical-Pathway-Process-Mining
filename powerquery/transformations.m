let
    // 1. Load Raw Source
    Source = Csv.Document(File.Contents("mock_hospital_logs.csv"), [Delimiter=",", Columns=6, Encoding=65001, QuoteStyle=QuoteStyle.None]),
    PromotedHeaders = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    
    // 2. Type Casting
    TypedTable = Table.TransformColumnTypes(PromotedHeaders, {
        {"Patient_ID", type text},
        {"Activity_Name", type text},
        {"Department", type text},
        {"Timestamp", type datetimezone},
        {"WaitTimeMinutes", Int64.Type},
        {"Status", type text}
    }),
    
    // 3. Null Replacement for Wait Times
    ReplacedNulls = Table.ReplaceValue(TypedTable, null, 0, Replacer.ReplaceValue, {"WaitTimeMinutes"}),
    
    // 4. Custom Column: Wait Time in Hours
    AddedWaitHours = Table.AddColumn(ReplacedNulls, "WaitTimeHours", each [WaitTimeMinutes] / 60, type number),
    
    // 5. Custom Column: Bottleneck Flag (> 60 mins)
    AddedBottleneckFlag = Table.AddColumn(AddedWaitHours, "Is_Bottleneck", each if [WaitTimeMinutes] > 60 then 1 else 0, Int64.Type)
in
    AddedBottleneckFlag

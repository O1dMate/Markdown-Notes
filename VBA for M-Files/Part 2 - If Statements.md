Dim a
Dim b
Dim c
Dim result
Dim currencyType

a = cDbl (Vault.ObjectPropertyOperations.GetProperty(ObjVer, vault.PropertyDefOperations.GetPropertyDefIDByAlias ("A")).TypedValue.DisplayValue)
b = cDbl (Vault.ObjectPropertyOperations.GetProperty(ObjVer, vault.PropertyDefOperations.GetPropertyDefIDByAlias ("B")).TypedValue.DisplayValue)
c = cDbl (Vault.ObjectPropertyOperations.GetProperty(ObjVer, vault.PropertyDefOperations.GetPropertyDefIDByAlias ("C")).TypedValue.DisplayValue)
currencyType = Vault.ObjectPropertyOperations.GetProperty(ObjVer, vault.PropertyDefOperations.GetPropertyDefIDByAlias ("testCurrency")).TypedValue.DisplayValue

result = (a*b) / c

If (InStr(currencyType, "Australian Dollars")) Then
  Output = "$" & Round(result, 4)
ElseIf (InStr(currencyType, "Euros")) Then
  Output = "€" & Round(result, 4)
ElseIf (InStr(currencyType, "Pounds")) Then
  Output = "£" & Round(result, 4)
Else 
  Output = "No Currency Selected"
End If
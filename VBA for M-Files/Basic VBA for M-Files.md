# Basic VBA for M-Files

### Loading & Returning Values
```vba
Dim a
Dim b
Dim c
Dim result
Dim currencyType

a = cDbl (Vault.ObjectPropertyOperations.GetProperty(ObjVer, vault.PropertyDefOperations.GetPropertyDefIDByAlias ("A")).TypedValue.DisplayValue)
b = cDbl (Vault.ObjectPropertyOperations.GetProperty(ObjVer, vault.PropertyDefOperations.GetPropertyDefIDByAlias ("B")).TypedValue.DisplayValue)
c = cDbl (Vault.ObjectPropertyOperations.GetProperty(ObjVer, vault.PropertyDefOperations.GetPropertyDefIDByAlias ("C")).TypedValue.DisplayValue)
currencyType = Vault.ObjectPropertyOperations.GetProperty(ObjVer, vault.PropertyDefOperations.GetPropertyDefIDByAlias ("currentType")).TypedValue.DisplayValue

result = (a*b) / c

Output = "$" & Round(result, 4) & " " & currencyType
```


### If Statements
```vba
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
```

### Functions
```vba
Dim a
Dim b
Dim c
Dim result
Dim currencyType

Function calculations(val1, val2, val3)
	calculations = (val1 * val2) / val3
End Function

a = cDbl (Vault.ObjectPropertyOperations.GetProperty(ObjVer, vault.PropertyDefOperations.GetPropertyDefIDByAlias ("A")).TypedValue.DisplayValue)
b = cDbl (Vault.ObjectPropertyOperations.GetProperty(ObjVer, vault.PropertyDefOperations.GetPropertyDefIDByAlias ("B")).TypedValue.DisplayValue)
c = cDbl (Vault.ObjectPropertyOperations.GetProperty(ObjVer, vault.PropertyDefOperations.GetPropertyDefIDByAlias ("C")).TypedValue.DisplayValue)
currencyType = Vault.ObjectPropertyOperations.GetProperty(ObjVer, vault.PropertyDefOperations.GetPropertyDefIDByAlias ("testCurrency")).TypedValue.DisplayValue

result = calculations(a, b, c)

Output = Round(result, 4) & " " & currencyType
```


### Default Values & Nested If Statements

```vba
If Not IsDate(InvoiceDate) Then
	Output = ""
Else
	If Not IsNumeric(PaymentTerms) Then
		Output = ""
	Else
		PaymentTerms = cDbl(PaymentTerms)

		DateFormat = FormatDateTime(InvoiceDate,2)

		Output = DateAdd("d",PaymentTerms,DateFormat)
	EndIf
End If
```
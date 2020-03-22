*** Settings ***
Library        DynamicTypesLibrary.py

*** Test Cases ***
Keyword Default Argument As Abject None
    ${return} =    DynamicTypesLibrary.Keyword None    ${None}
    Should Match Regexp    ${return}    None: <(class|type) 'NoneType'>

Keyword Default Argument As Abject None Default Value
    ${return} =    DynamicTypesLibrary.Keyword None
    Should Match Regexp    ${return}    None: <(class|type) 'NoneType'>

Keyword Default Argument As String None
    ${return} =    DynamicTypesLibrary.Keyword None    None
    Should Match Regexp    ${return}    None: <(class|type) 'NoneType'>

Keyword Default As Booleans With Defaults
    ${return}    DynamicTypesLibrary.Keyword Booleans
    Should Match Regexp    ${return}    True: <(class|type) 'bool'>, False: <(class|type) 'bool'>

Keyword Default As Booleans With Strings
    ${return} =    DynamicTypesLibrary.Keyword Booleans    False    True
    Should Match Regexp    ${return}    False: <(class|type) 'bool'>, True: <(class|type) 'bool'>

Keyword Default As Booleans With Objects
    ${return} =    DynamicTypesLibrary.Keyword Booleans    ${False}    ${True}
    Should Match Regexp    ${return}    False: <(class|type) 'bool'>, True: <(class|type) 'bool'>

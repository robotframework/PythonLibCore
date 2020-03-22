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
    ${arg1}    ${arg2} =    DynamicTypesLibrary.Keyword Booleans
    Should Be Equal    ${arg1}    ${True}
    Should Be Equal    ${arg2}    ${False}

Keyword Default As Booleans With Strings
    ${arg1}    ${arg2} =    DynamicTypesLibrary.Keyword Booleans    False    True
    Should Be Equal    ${arg1}    ${False}
    Should Be Equal    ${arg2}    ${True}

Keyword Default As Booleans With Objects
    ${arg1}    ${arg2} =    DynamicTypesLibrary.Keyword Booleans    ${False}    ${True}
    Should Be Equal    ${arg1}    ${False}
    Should Be Equal    ${arg2}    ${True}

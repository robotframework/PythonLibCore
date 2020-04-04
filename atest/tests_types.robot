*** Settings ***
Library        DynamicTypesLibrary.py
Suite Setup    Import DynamicTypesAnnotationsLibrary In Python 3 Only

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

Keyword Annonations And Bool Defaults Using Default
    [Tags]    py3
    ${return} =    DynamicTypesAnnotationsLibrary.Keyword Default And Annotation    42
    Should Match Regexp    ${return}    42: <(class|type) 'int'>, False: <(class|type) 'bool'>

Keyword Annonations And Bool Defaults Defining All Arguments
    [Tags]    py3
    ${return} =    DynamicTypesAnnotationsLibrary.Keyword Default And Annotation    1    true
    Should Match Regexp    ${return}    1: <(class|type) 'int'>, True: <(class|type) 'bool'>

Keyword Annonations And Bool Defaults Defining All Arguments And With Number
    [Tags]    py3
    ${return} =    DynamicTypesAnnotationsLibrary.Keyword Default And Annotation    ${1}    true
    Should Match Regexp    ${return}    1: <(class|type) 'int'>, True: <(class|type) 'bool'>

Keyword Annonations And Robot Types Disbales Argument Conversion
    [Tags]    py3
    ${return} =    DynamicTypesAnnotationsLibrary.Keyword Robot Types Disabled And Annotations    111
    Should Match Regexp    ${return}    111: <(class|type) 'str'>

Keyword Annonations And Robot Types Defined
    [Tags]    py3
    ${return} =    DynamicTypesAnnotationsLibrary.Keyword Robot Types And Bool Defaults    tidii    111
    Should Match Regexp    ${return}    tidii: <(class|type) 'str'>, 111: <(class|type) 'str'>

Keyword Annonations And Keyword Only Arguments
    [Tags]    py3
    ${return} =    DynamicTypesAnnotationsLibrary.Keyword Only Arguments    1    ${1}    some=222
    Should Match    ${return}    ('1', 1): <class 'tuple'>, 222: <class 'int'>

*** Keywords ***
Import DynamicTypesAnnotationsLibrary In Python 3 Only
    ${py3} =    DynamicTypesLibrary.Is Python 3
    Run Keyword If     ${py3}
    ...    Import Library      DynamicTypesAnnotationsLibrary.py    Dummy

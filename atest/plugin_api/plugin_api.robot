*** Test Cases ***
Plugin Test
    Import Library    ${CURDIR}/PluginLib.py    plugins=${CURDIR}/MyPlugin.py
    ${value} =    Foo
    Should Be Equal    ${value}    ${1}
    ${value} =    Plugin Keyword
    Should Be Equal    ${value}    ${2}

Plugins With Base Class
    Import Library    ${CURDIR}/PluginWithBaseLib.py    plugins=${CURDIR}/MyPluginBase.py
    ${value} =    Base Plugin Keyword
    Should Be Equal    ${value}    40
    ${value} =    Base Keyword
    Should Be Equal    ${value}    42

Pugins With No Base Class
    Run Keyword And Expect Error
    ...    *PluginError: Plugin does not inherit <class 'PluginWithBaseLib.BaseClass'>
    ...    Import Library    ${CURDIR}/PluginWithBaseLib.py    plugins=${CURDIR}/MyPlugin.py

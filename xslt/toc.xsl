<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns="http://www.w3.org/1999/xhtml"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:tei="http://www.tei-c.org/ns/1.0"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:local="http://dse-static.foo.bar"
    version="2.0" exclude-result-prefixes="xsl tei xs local">
    <xsl:output encoding="UTF-8" media-type="text/html" method="html" version="5.0" indent="yes" omit-xml-declaration="yes"/>
    
    <xsl:import href="partials/html_navbar.xsl"/>
    <xsl:import href="partials/html_head.xsl"/>
    <xsl:import href="partials/html_footer.xsl"/>
    <xsl:import href="partials/tabulator_dl_buttons.xsl"/>
    <xsl:import href="partials/tabulator_js.xsl"/>
    <xsl:import href="partials/breadcrumbs.xsl"/>


    <xsl:template match="/">
        <xsl:variable name="doc_title" select="'Inhaltsverzeichnis'"/>
        <html class="h-100" lang="de">
            <head>
                <xsl:call-template name="html_head">
                    <xsl:with-param name="html_title" select="$doc_title"></xsl:with-param>
                </xsl:call-template>
            </head>
            
            <body class="d-flex flex-column h-100">
            <xsl:call-template name="nav_bar"/>
                <main class="flex-shrink-0 flex-grow-1">
                
                    <xsl:call-template name="breadcrumb">
                        <xsl:with-param name="breadcrumb_item" select="'Sitzungsprotokolle'" />
                    </xsl:call-template>

                    <div class="container">
                        <h1>Inhaltsverzeichnis</h1>
                        <table id="myTable">
                            <thead>
                                <tr>
                                    <th scope="col">Titel</th>
                                    <th scope="col">Sitzung</th>
                                    <th scope="col">Gesetzgebungsperiode</th>
                                    <th scope="col">Datum</th>
                                    <th scope="col">URL</th>
                                </tr>
                            </thead>
                            <tbody>
                                <xsl:for-each
                                    select="collection('../data/editions?select=*.xml')//tei:TEI">
                                    <xsl:variable name="full_path">
                                        <xsl:value-of select="document-uri(/)"/>
                                    </xsl:variable>
                                    <tr>
                                        <td>
                                             <xsl:value-of
                                                select=".//tei:titleStmt/tei:title[@type='sub'][1]/text()"/>
                                        </td>
                                         <td>
                                            <xsl:value-of select=".//tei:titleStmt/tei:meeting[1]/text()"/>
                                        </td>
                                        <td>
                                            <xsl:value-of select=".//tei:titleStmt/tei:meeting[2]/text()"/>
                                        </td>
                                        <td>
                                            <xsl:value-of
                                                select=".//tei:settingDesc/tei:setting/tei:date/text()"/>
                                        </td>
                                        <td>
                                        <xsl:value-of
                                                  select="replace(tokenize($full_path, '/')[last()], '.xml', '.html')"
                                                  />
                                        </td>
                                    </tr>
                                </xsl:for-each>
                            </tbody>
                        </table>
                        <xsl:call-template name="tabulator_dl_buttons"/>
                    </div>
                </main>
                <xsl:call-template name="html_footer"/>
                <xsl:call-template name="tabulator_js">
                    <xsl:with-param name="column_def">
                        <xsl:text>
                        [{title: "Titel", minWidth: 300, headerFilter: "input", formatter: linkFormatter, formatterParams:{fieldName: "titel"}},
                        {title: "Sitzung", headerFilter: "input"},
                        {title: "Gesetzgebungsperiode", headerFilter: "input"},
                        {title: "Datum", headerFilter: "input"},
                        {title: "URL", visible:false}]
                        </xsl:text>
                    </xsl:with-param>
                </xsl:call-template>
            </body>
        </html>
    </xsl:template>
</xsl:stylesheet>

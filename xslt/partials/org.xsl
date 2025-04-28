<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema"
    xmlns:tei="http://www.tei-c.org/ns/1.0" version="2.0" exclude-result-prefixes="xsl tei xs">

    <xsl:import href="tabulator_dl_buttons.xsl"/>
    <xsl:template match="tei:org" name="org_detail">
        <table class="table entity-table">
            <tbody>
                <xsl:if test="./tei:orgName">
                    <tr>
                        <th>
                            Name
                        </th>
                        <td>
                            <xsl:value-of select="./tei:orgName"/>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="./tei:desc">
                    <tr>
                        <th>
                            Beschreibung
                        </th>
                        <td>
                            <xsl:value-of select="./tei:desc"/>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="./tei:idno[@type='GND']">
                    <tr>
                        <th>
                            GND
                        </th>
                        <td>
                            <a href="{./tei:idno[@type='GND']}" target="_blank">
                                <xsl:value-of select="tokenize(./tei:idno[@type='GND'], '/')[last()]"/>
                            </a>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="./tei:idno[@subtype='wikidata']">
                    <tr>
                        <th>
                            Wikidata ID
                        </th>
                        <td>
                            <a href="{./tei:idno[@subtype='wikidata']}" target="_blank">
                                <xsl:value-of select="tokenize(./tei:idno[@subtype='wikidata'], '/')[last()]"/>
                            </a>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="./tei:idno[@type='GEONAMES']">
                    <tr>
                        <th>
                        Geonames ID
                        </th>
                        <td>
                            <a href="{./tei:idno[@type='GEONAMES']}" target="_blank">
                                <xsl:value-of select="tokenize(./tei:idno[@type='GEONAMES'], '/')[4]"/>
                            </a>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="./tei:note">
                    <tr>
                        <th>
                            Notiz
                        </th>
                        <td>
                            <xsl:value-of select="./tei:note"/>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:if test="./tei:noteGrp/tei:note[@type='mentions']">
                    <tr>
                        <th>
                            Erwähnt in
                        </th>
                        <td>
                            <ul>
                                <xsl:for-each select="./tei:noteGrp/tei:note[@type='mentions']">
                                    <li>
                                        <a href="{replace(@target, '.xml', '.html')}">
                                            <xsl:value-of select="./text()"/>
                                        </a>
                                    </li>
                                </xsl:for-each>
                            </ul>
                        </td>
                    </tr>
                </xsl:if>
                <xsl:variable name="org-id" select="./@xml:id"/>
                <xsl:variable name="org-ref" select="concat('#', $org-id)"/>
                <xsl:variable name="relations" select="//tei:listRelation/tei:relation[@active=$org-ref]"/>
                <xsl:if test="$relations">
                    <tr>
                        <th>Personen</th>
                        <td>
                            <table id="myTable">
                                <thead>
                                    <tr>
                                        <th scope="col">Name</th>
                                        <th scope="col">Rolle</th>
                                        <th scope="col">Zeitraum</th>
                                        <th scope="col">URL</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <xsl:for-each select="$relations">
                                        <xsl:variable name="person-id" select="substring-after(@passive, '#')"/>
                                        <tr>
                                            <td>
                                                <xsl:value-of select="normalize-space(string-join(//tei:standOff/tei:listPerson/tei:person[@xml:id=$person-id]/tei:persName[1]//text()))"/>
                                            </td>
                                            <td>
                                                <xsl:if test="./tei:desc">
                                                    <xsl:choose>
                                                        <xsl:when test="./tei:desc[@xml:lang='de']">
                                                            <xsl:value-of select="./tei:desc[@xml:lang='de']"/>
                                                        </xsl:when>
                                                        <xsl:otherwise>
                                                            <xsl:value-of select="./tei:desc[1]"/>
                                                        </xsl:otherwise>
                                                    </xsl:choose>
                                                </xsl:if>
                                            </td>
                                            <td>
                                                <xsl:if test="@from or @to">
                                                    <xsl:if test="@from">
                                                        <xsl:value-of select="@from"/>
                                                    </xsl:if>
                                                    <xsl:if test="@from and @to">
                                                        <xsl:text> - </xsl:text>
                                                    </xsl:if>
                                                    <xsl:if test="@to">
                                                        <xsl:value-of select="@to"/>
                                                    </xsl:if>
                                                </xsl:if>
                                            </td>
                                            <td>
                                                <xsl:value-of select="concat($person-id, '.html')"/>
                                            </td>
                                        </tr>
                                    </xsl:for-each>
                                </tbody>
                            </table>
                            <xsl:call-template name="tabulator_dl_buttons"/>
                        </td>
                    </tr>
                </xsl:if>
            </tbody>
        </table>
    </xsl:template>
</xsl:stylesheet>

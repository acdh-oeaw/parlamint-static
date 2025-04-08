<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    xmlns:xs="http://www.w3.org/2001/XMLSchema" xmlns:tei="http://www.tei-c.org/ns/1.0"
    version="2.0" exclude-result-prefixes="xsl tei xs">

    <xsl:template match="tei:person" name="person_detail">
        <div class="row">
            <div class="col-md-4">
                <xsl:choose>
                    <xsl:when test=".//tei:graphic/@url">
                        <xsl:variable name="imgurl">
                            <xsl:value-of select=".//tei:graphic/@url"/>
                        </xsl:variable>
                        <figure class="figure">
                            <img src="{$imgurl}" class="figure-img img-fluid rounded wikidataimage" alt="" />
                            <figcaption class="figure-caption">Wikidata-Bild</figcaption>
                        </figure>
                    </xsl:when>
                    <xsl:otherwise>
                        <p>Keine Abbildung vorhanden</p>
                    </xsl:otherwise>
                </xsl:choose>
                
            </div>
            <div class="col-md-8">
                <dl>
                    <xsl:if test="./tei:birth/@when">
                        <dt>
                            Geboren
                        </dt>
                        <dd>
                            <xsl:if test="./tei:birth/tei:placeName">
                                <xsl:value-of select=".//tei:birth/tei:placeName/text()"/>
                            </xsl:if>
                            <xsl:if test="./tei:birth/@when">
                                <xsl:text>, </xsl:text><xsl:value-of select="./tei:birth/@when"/>
                            </xsl:if>
                        </dd>
                    </xsl:if>
                    
                    <xsl:if test="./tei:death/@when">
                        <dt>
                            Gestorben
                        </dt>
                        <dd>
                            <xsl:if test="./tei:death/tei:placeName">
                                <xsl:value-of select=".//tei:death/tei:placeName/text()"/>
                            </xsl:if>
                            <xsl:if test="./tei:death/@when">
                                <xsl:if test="./tei:death/tei:placeName">
                                    <xsl:text>, </xsl:text>
                                </xsl:if>
                                <xsl:value-of select="./tei:death/@when"/>
                            </xsl:if>
                        </dd>
                    </xsl:if>
                    
                    <xsl:if test="./tei:affiliation[./tei:roleName]">
                        <dt>Funktionen</dt>
                        <xsl:for-each select="./tei:affiliation[./tei:roleName[@xml:lang='de']]">
                            <dd>
                                <xsl:value-of select="./tei:roleName[@xml:lang='de']"/> (<xsl:value-of select=".//@from"/>–<xsl:value-of select=".//@to"/>)
                            </dd>
                        </xsl:for-each>
                    </xsl:if>
                    
                    <xsl:if test="./tei:affiliation[not(./tei:roleName)]">
                        <dt>Parteimitgliedschaften</dt>
                        <xsl:for-each select="./tei:affiliation[starts-with(@ref, '#parliamentaryGroup')]">
                            <dd>
                                <xsl:value-of select="data(./@ref)"/> (<xsl:value-of select=".//@from"/>–<xsl:value-of select=".//@to"/>)
                            </dd>
                        </xsl:for-each>
                    </xsl:if>
                </dl>
            </div>
            
        </div>
        <hr />
        <xsl:if test="./tei:noteGrp/tei:note[@type = 'mentions']">
            <h2>Erwähnt in</h2>
            <ul>
            <xsl:for-each select="./tei:noteGrp/tei:note[@type = 'mentions']">
                <li>
                    <a href="{replace(@target, '.xml', '.html')}">
                        <xsl:value-of select="./text()"/>
                    </a>
                </li>
            </xsl:for-each>
            </ul>
        </xsl:if>

    </xsl:template>
</xsl:stylesheet>

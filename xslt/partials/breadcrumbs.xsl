<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet xmlns="http://www.w3.org/1999/xhtml"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="2.0">

    <xsl:template name="breadcrumb">
        <xsl:param name="breadcrumb_item" />
        <xsl:param name="parent_page_link"/>
        <nav style="--bs-breadcrumb-divider: '>';" aria-label="breadcrumb" class="ps-5 p-3">
            <ol class="breadcrumb">
                <li class="breadcrumb-item">
                    <a href="index.html">ParlaMint-AT</a>
                </li>
                <xsl:choose>
                    <xsl:when test="$parent_page_link">
                        <li class="breadcrumb-item" aria-current="page">
                            <a href="{$parent_page_link}">
                                <xsl:value-of select="$breadcrumb_item"/>
                            </a>
                        </li>
                    </xsl:when>
                    <xsl:otherwise>
                        <li class="breadcrumb-item active" aria-current="page">
                            <xsl:value-of select="$breadcrumb_item"/>
                        </li>
                    </xsl:otherwise>
                </xsl:choose>
            </ol>
        </nav>
    </xsl:template>
</xsl:stylesheet>
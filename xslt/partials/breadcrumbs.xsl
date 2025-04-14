<?xml version="1.0" encoding="UTF-8"?>
<xsl:stylesheet 
    xmlns="http://www.w3.org/1999/xhtml"
    xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
    version="2.0">
    
    <xsl:template name="breadcrumb">
        <xsl:param name="current_page" />
        <nav style="--bs-breadcrumb-divider: '>';" aria-label="breadcrumb" class="ps-5 p-3">
            <ol class="breadcrumb">
                <li class="breadcrumb-item">
                    <a href="index.html">ParlaMint-AT</a>
                </li>
                <li class="breadcrumb-item active" aria-current="page">
                    <xsl:value-of select="$current_page" />
                </li>
            </ol>
        </nav>
    </xsl:template>
</xsl:stylesheet>
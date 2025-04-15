// holds shared config for all tabulator-js tables
function linkFormatter(cell, formatterParams, onRendered){
    const cellData = cell.getData();
    const rowData = cell.getRow().getData();
    const url = rowData.url
    const fieldName = formatterParams.fieldName;
    const theLink = `<a href="${url}">${cellData[fieldName]}</a>`;
    return theLink;
    }
var config = {
    height: 800,
    layout: "fitColumns",
    tooltips: true,
    dataLoader: true,
};

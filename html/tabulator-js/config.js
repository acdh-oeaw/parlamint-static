// holds shared config for all tabulator-js tables
function linkFormatter(cell) {
    const cellData = cell.getData();
    const rowData = cell.getRow().getData();
    const url = rowData.url
    const theLink = `<a href="${url}">${cellData.titel}</a>`;
    return theLink;
    }
var config = {
    height: 800,
    layout: "fitColumns",
    tooltips: true,
    dataLoader: true,
};

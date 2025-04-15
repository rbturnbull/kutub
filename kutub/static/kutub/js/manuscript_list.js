const deleteAssetButton = (params) => {    
  const link = document.createElement('a');
  link.innerHTML = '<i class="fa-solid fa-trash-can" style="color: red;"></i>';
  link.href= params.value;
  return link;
}

const dateSorter = (date1Str, date2Str) => {
  const date1 = Date.parse(date1Str);
  const date2 = Date.parse(date2Str);    
  if(date1 === null && date2 === null) return 0;
  if(date1 === null) return -1;
  if(date2 === null) return 1;    
  return date1 - date2;    
}

const linkRenderer = (params) => {  
  const span = document.createElement("span");
  span.innerHTML = params.value
  return span;
}

const sourceRenderer = (params) => {
  if(params.value){
    console.log(params)
    const a = document.createElement("a");
    a.href = params.value;
    a.textContent = "Source";
    a.target = "_blank";
    return a;
  }
  return "";
}

const setupManuscriptList= (manuscripts = []) => {  
  let rowData = [];
  manuscripts.forEach(manuscript => {
      rowData.push(manuscript);
  });
  const gridOptions = {
      rowData: rowData,
      columnDefs: [
          { field: "heading", flex: 1, cellRenderer: linkRenderer},
          { field: "identifier", flex: 1 },                  
          { field: "repository", flex: 1, cellRenderer: linkRenderer},
          { field: "source", flex: 1, cellRenderer: sourceRenderer}
      ]        
  };
  const myGridElement = document.querySelector('#manuscript-manage-grid');
  let gridApi = agGrid.createGrid(myGridElement, gridOptions);
  let searchInput = document.querySelector('#manuscript-search');
  searchInput.addEventListener("input", (e) => {
      let query = e.target.value;
      gridApi.setGridOption("quickFilterText", query);
  })
}

export {setupManuscriptList}
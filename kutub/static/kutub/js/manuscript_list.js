const getNumber = (str) => {
  const match = str && str.match(/\d+/);
  return match ? parseInt(match[0], 10) : null;
};

const identifierSorter = (id1, id2) => {
  // Extract numbers from the identifiers if they exist  
  
  const num1 = getNumber(id1);
  const num2 = getNumber(id2);
  
  // If both have numbers, compare numerically
  if (num1 !== null && num2 !== null) {
    return num1 - num2;
  }
  // If only one has a number, prioritize the one with a number
  if (num1 !== null) return -1;
  if (num2 !== null) return 1;
  
  // Otherwise, compare alphabetically
  return (id1 || '').localeCompare(id2 || '');
};

const linkRenderer = (params) => {  
  const span = document.createElement("span");
  span.innerHTML = params.value
  return span;
}

const sourceRenderer = (params) => {
  if(params.value){    
    const a = document.createElement("a");
    a.href = params.value;
    a.textContent = "Source";
    a.target = "_blank";
    return a;
  }
  return "";
}

const setupManuscriptList= (manuscripts = []) => {  
  console.log('setting up table');
  let rowData = [];
  manuscripts.forEach(manuscript => {
      rowData.push(manuscript);
  });
  const gridOptions = {
      rowData: rowData,
      columnDefs: [
          { field: "heading", flex: 1, cellRenderer: linkRenderer, rowDrag: true},
          { field: "identifier", flex: 1, comparator: identifierSorter },                  
          { field: "internal identifier", flex: 1},
          { field: "repository", flex: 1, cellRenderer: linkRenderer},
          { field: "source", flex: 1, cellRenderer: sourceRenderer},          
      ],
      rowDragManaged: true,       
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
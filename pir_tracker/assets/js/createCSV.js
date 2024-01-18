function dicoToFormatCSV(dico){

    const titleKeys = Object.keys(dico[0])
  
    const refinedData = []
    refinedData.push(titleKeys)

    dico.forEach(item => {
        refinedData.push(Object.values(item))  
    })

    let csvContent = ''

    refinedData.forEach(row => {
    csvContent += row.join(';') + '\n'
    })
    return csvContent;
}

function dataToCSV(csvContent, nomDiv){
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8,' })
    const objUrl = URL.createObjectURL(blob)
    
    const link = document.createElement('a')
    link.setAttribute('href', objUrl)

    if (nomDiv == "allEvents"){
      link.setAttribute('download', 'allEvents.csv')
      link.textContent = 'Download all events'
    }
    if (nomDiv == "mouseMoveEvents"){
      link.setAttribute('download', 'mouseMoveEvents.csv')
      link.textContent = 'Download mouse move events'
    }
    
    document.getElementById(nomDiv).append(link)

}


/**************** import csv  **************** */

/*
const ourData = [
  {
    temps:dico.JSON,
    lastName: 'Udoh',
    test:'rddd'
  },
  {
    firstName: 'Loyle',
    lastName: 'Carner'
  },
  {
    firstName: 'Tamunotekena',
    lastName: 'Dagogo'
  }
]

let csvContent = dicoToFormatCSV(ourData);
dataToCSV(csvContent);
*/

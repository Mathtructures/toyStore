function addRemove(e){
    const dataset = e.currentTarget.dataset
    const type = dataset.type
    const id = parseInt(dataset.id)
    const action = dataset.action
    const baseUrl = document.location.protocol + '//' + document.location.host
    // alert(dataset.type + ' ' + dataset.id)
    fetch(`${baseUrl}/cartoperation${type}${id}${action}${0}`)
    .then(response => response.json())
    .then(data => proccess(data))
}

function proccess(data){
    alert(data.respMessage)
}
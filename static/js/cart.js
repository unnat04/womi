var updateBtns=document.getElementsByClassName('update-cart')

for(var i=0;i<updateBtns.length;i++){
    updateBtns[i].addEventListener('click',function(){
        var productId=this.dataset.product
        var action = this.dataset.action
        console.log('productId:',productId,'action:',action)

        console.log('USER:',user)
        if(user==='AnonymousUser'){
            addCookieItem(productId,action)
        }
        else{
            updateUserOrder(productId,action)
        }
    })
}

function addCookieItem(productID,action){
    console.log('Not Logged in!...')

    if(action=='add'){
        if(cart[productID] == undefined){
            cart[productID]={'quantity':1}
        }else{
            cart[productID]['quantity'] += 1
        }
    }

    if(action=='remove'){
        cart[productID]['quantity'] -= 1
        if(cart[productID]['quantity']<=0){
            console.log('Remove Item')
            delete cart[productID]
        }
    }
    console.log('Cart:',cart)
    document.cookie='cart='+JSON.stringify(cart)+";domain=;path=/"
    location.reload()
}

function updateUserOrder(productId,action){
    console.log('User is logged in, sending data....')

    var url='/update_item/'

    fetch(url,{method:'POST',headers:{'Content-Type':'application/json','X-CSRFToken':csrftoken},body:JSON.stringify({'productID':productId,'action':action})})
    
    .then((response)=>{
        return response.json()
    })

    .then((data)=>{
        console.log('data',data)
        location.reload()
    })

}
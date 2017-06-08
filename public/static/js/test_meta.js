(function e(t,n,r){function s(o,u){if(!n[o]){if(!t[o]){var a=typeof require=="function"&&require;if(!u&&a)return a(o,!0);if(i)return i(o,!0);var f=new Error("Cannot find module '"+o+"'");throw f.code="MODULE_NOT_FOUND",f}var l=n[o]={exports:{}};t[o][0].call(l.exports,function(e){var n=t[o][1][e];return s(n?n:e)},l,l.exports,e,t,n,r)}return n[o].exports}var i=typeof require=="function"&&require;for(var o=0;o<r.length;o++)s(r[o]);return s})({1:[function(require,module,exports){
 var web3 = new Web3();
  window.addEventListener('load', function() {

  // Checking if Web3 has been injected by the browser (Mist/MetaMask)
  if (typeof web3 !== 'undefined') {
    // Use Mist/MetaMask's provider
    window.web3 = new Web3(web3.currentProvider);
  } else {
    console.log('No web3? You should consider trying MetaMask!')
    // fallback - use your fallback strategy (local node / hosted node + in-dapp id mgmt / fail)
    window.web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
  }



function hex2a(hexx) {
    var hex = hexx.toString();//force conversion
    var str = '';
    for (var i = 0; i < hex.length; i += 2)
        str += String.fromCharCode(parseInt(hex.substr(i, 2), 16));
    return str;
}

  // Now you can start your app & access web3 freely:
 console.log(web3.eth.accounts[0]);
 var account = web3.eth.accounts[0];
var accountInterval = setInterval(function() {
  if (web3.eth.accounts[0] !== account) {
    account = web3.eth.accounts[0];
    console.log(account);
  }
}, 100);

//  web3.eth.getTransactionFromBlock("0x383dfab3f35d3a4420a19c4ee3a1034997f079d1907cd98390d64d5de4b91ceb", function(error, result){
//     if(!error){
//         console.log(result);
//       console.log((result.input.substring(404)));
//       console.log(hex2a(result.input.substring(404)));
//     }
//     else
//         console.error(error);
// });

//   web3.eth.getTransaction("0x3ded18992646a4131fbafcc209ed51ddbe91da6b7a23d3181197da97b076c175", function(error, result){
//     if(!error){
//         console.log(result.value.s);
//     }
//     else
//         console.error(error);
// });

var restaurantContract = web3.eth.contract([{"constant":false,"inputs":[{"name":"com","type":"string"}],"name":"commente","outputs":[{"name":"ok","type":"bool"}],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"kill","outputs":[],"payable":false,"type":"function"},{"constant":false,"inputs":[],"name":"paieAddition","outputs":[],"payable":true,"type":"function"},{"constant":true,"inputs":[],"name":"chiffreAffaire","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"comments","outputs":[{"name":"addr","type":"address"},{"name":"message","type":"string"},{"name":"date","type":"uint256"}],"payable":false,"type":"function"},{"constant":true,"inputs":[],"name":"nbComments","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function"},{"inputs":[{"name":"premium","type":"bool"}],"payable":false,"type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"out","type":"address"}],"name":"Print","type":"event"}]);

var restaurant = restaurantContract.at("0xA831310b240f4B4acDFd2E8E8afA462Ad6578F71");
restaurant.comments.call(0,function(error, result){
    if(!error){
        console.log(result);
    }
    else
        console.error(error);
});

  function paieRestaurant(){
    var montant = document.getElementById("addition").value ;
    console.log(montant);
    var block = restaurant.paieAddition.sendTransaction({from:account,value:web3.toWei(montant, "ether")}, function(err, address) {
    if (!err)
      console.log(address); //0x3ded18992646a4131fbafcc209ed51ddbe91da6b7a23d3181197da97b076c175
    });
  }

  function commenter(){
    var com = document.getElementById("commentaire").value ;
    console.log(com);
    var block = restaurant.commente.sendTransaction(com,{from:account,gas:210000}, function(err, address) {
    if (!err)
      console.log(address); //0x3ded18992646a4131fbafcc209ed51ddbe91da6b7a23d3181197da97b076c175
    });
  }


document.getElementById("button1").addEventListener("click", paieRestaurant);
document.getElementById("button2").addEventListener("click", commenter);

})

},{}]},{},[1]);

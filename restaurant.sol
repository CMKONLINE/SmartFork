pragma solidity ^0.4.0;
/*
- stockage transaction via web3 : getTransaction (sauvegarde du hash à l'extérieur de la blockchain)
- signature du commentaire à l'extérieur de la blockchain également à sauver
*/
contract Restaurant {
    uint public chiffreAffaire=0;
    address restaurantWallet;
    bool estPremium;
    address private constant smartFork = 0xBE965ADE05180186CDEeb1b31d4694BF5f4A55cB;
    
    function Restaurant(bool premium){
        restaurantWallet=msg.sender;
        estPremium=premium;
    }
    struct Commentaire {
        address addr;
        string message;
        uint date;
    }
    struct Transaction {
        address addr;
        uint amount;
        uint date;
        Commentaire c;
    }
    event Print(address out);// a supprimer

    mapping (address => Transaction []) transactions;
    mapping (uint => Commentaire) public comments;
    uint public nbComments=0;
    
    function paieAddition() payable {
        if (msg.value > 1 ether){// montant minimum sur la facture
            transactions[msg.sender].push(Transaction({addr: msg.sender, amount: msg.value,date:now,c:Commentaire({addr: msg.sender,message:"",date:now})}));
            chiffreAffaire+=msg.value;
        }
    }

    function commente(string com) returns(bool ok){
        if (transactions[msg.sender].length>0){
            Transaction [] tab= transactions[msg.sender];
            Transaction trans = tab[tab.length-1];
            Commentaire comment = trans.c;
            bytes mess=bytes (comment.message);//pour avoir la longueur du commentaire : conversion en bytes
            uint date1=now;
            if((mess.length==0) && (date1-trans.date<7 days)){
                // verifie aussi qu on n a pas deja poste un commentaire pour cette transaction
                // et que le commentaire a lieu dans la semaine suivant la transaction
                comments[nbComments]=Commentaire({addr: msg.sender, message: com,date:date1});
                trans.c=comments[nbComments++];
                Print(msg.sender);// a supprimer
                if (estPremium){
                    //si le restaurant est premium, ristourne pour le client car il a poste un commentaire
                    address ad = trans.addr;
                    uint ristourne = trans.amount/10;
                    if (!ad.send(ristourne)){
                        return false;
                    }
                    else{
                        chiffreAffaire-=ristourne;
                        uint feeSmartFork=trans.amount/50;
                        if (smartFork.send(feeSmartFork))
                            chiffreAffaire -= feeSmartFork;
                    }
                }
                return true;
            }
        }
        else return false;
    }

    
    function kill(){
        if (msg.sender == restaurantWallet)
            suicide(restaurantWallet);  // kills this contract and sends remaining funds back to restaurantWallet
    } 
}

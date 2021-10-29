let FileOrName = 'E:/coop6/Coop-main/data/user_selected.osm'; // "Ivano-Frankivsk, Ivano-Frankivsk, Ukraine"
let NCars = 4;


module.exports ={
    setFileOrName: function(fileOrName){
        FileOrName = fileOrName
    },
    setNCars: function(nCars){
        NCars = nCars
    },
    getFileOrName: function() { return FileOrName },
    getNCars: function() { return NCars}

};





















let FileOrName = '/Users/a1/Desktop/turik/data/user_selected.osm'; // "Ivano-Frankivsk, Ivano-Frankivsk, Ukraine"
let NCars = 10;


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

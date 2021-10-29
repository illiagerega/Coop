let FileOrName = 'Ivano-Frankivsk, Ivano-Frankivsk, Ukraine'; // "Ivano-Frankivsk, Ivano-Frankivsk, Ukraine"
let NCars = 3;


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




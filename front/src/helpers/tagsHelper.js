// dj server expects a sting of tags separated by comma
// however we need to clean user's input
// tagsHelp func trimInputTag: cleans tag string
//                             1.brings tags to lower case,
//                             2.removes comma at the end and 
//                             3.trims each tag

// tagsHelp converTagsListTo String: takes arr of tags => string

const  tagsHelp ={
    trimInputTag(initialString) {
        console.log('initial tags str',initialString)
      // get str input(items separ by ',') and return an cleaned string with items
      let idxLastComma = initialString.lastIndexOf(",");
      // get rid of possible , at the ens of input
      if (initialString.lastIndexOf(",") === initialString.length - 1) {
          console.log("inside if ")
        initialString = initialString.substr(0, idxLastComma).toLowerCase();
        console.log("result is",initialString)
      } 
      initialString.toLowerCase();
      let arrFromSplitStr = initialString.split(",");
      //console.log("check if you have , at the end", arrFromSplitStr);
      let collector = "";
      arrFromSplitStr.forEach((item) => {
        // console.log("item is",item)
        collector += `${item.trim()},`;
      });
      // return string
      return collector;
    },
    convertTagsListToString(arrTags) {
      //get tag arr and return str where tags separated by ',' 
      let collector = "";
      arrTags.forEach((item) => {
        console.log("item from convert is",item)
        collector += `${item.trim()},`;
      });
      console.log("Done, got a string",collector)
      return collector;
    }
  }
  
  
  
  export default tagsHelp
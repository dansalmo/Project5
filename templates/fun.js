function compress(str) {
    var count = 1;
    var compressed = "";
    for (i in str) {
        if str[i] != str[i+1] {
            compressed += str[i] + count;
            count = 1;
        } else {
            count++;
        }
    }
    return compressed

}
import book as b
def main():
    dataBook = []
    # 遍历10页内的图书信息
    for i in range(0, 10):
        gl = b.geturl('https://book.douban.com/top250?start={}'.format(i))
        pa = b.Parserdata(gl)
        dataBook.extend(pa)  # 把10页的书籍信息都保存在dataBook列表里面，统一保存
    # 存入到book文件夹
    b.savepoint(dataBook)
    # b.savemysql(dataBook)
    b.analysetime()
    b.analysescore()
    b.analysemon()
    b.anyciyun()
if __name__ == '__main__':
    main()


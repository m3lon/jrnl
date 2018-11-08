1. 想实现多行输入，通过循环解决 如何实现多行输入 按Ctrl+D解决呢？ 答：stdin
2. 对字符串的分析，标题与主题 title、content,通过正则？答：匹配到第一个特殊字符,能返回一个元组序列，通过序列解包赋值
3. 时间处理：使用time模块strftime格式化日期 答：通过dateparser模块 想封装为一个函数
4. 文件写入? 答：with as 关于file的一些参数
5. 存入格式："{time} {title} {content}".format_map(journal) 如何加入回车？答：print就好
6. 输出格式，直接读取文件行数  python参数解析库 抓住问题的关键 仿照下面的开始做 答：循环file.readline
    ```python
        import argparse

        parser = argparse.ArgumentParser()

        parser.add_argument("--square", help="display a square of a given number", type=int)
        parser.add_argument("--cubic", help="display a cubic of a given number", type=int)

        args = parser.parse_args()

        if args.square:
            print args.square**2

        if args.cubic:
            print args.cubic**3
    ```

    我想要的结构是定位参数与可选参数混合使用
    ```python
    import argparse

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('integers', metavar='N', type=int, nargs='+',
                    help='an integer for the accumulator')
    parser.add_argument('--sum', dest='accumulate', action='store_const',
                    const=sum, default=max,
                    help='sum the integers (default: find the max)')

    args = parser.parse_args()
    print args.accumulate(args.integers)
    ```
7. 关于时间处理，我有一些想法，目前方案有二：
    - 方案一：调用参数 -t 指定用户将输入时间参数 eg： jrnl -t yesterday at 3pm
    - 方案二：自动判断，首先需要确定以冒号分隔，再通过try...测试dateparser.parse()函数返回是否为空，若为空，则没有指定时间
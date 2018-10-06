# encoding: utf-8
import argparse
parser = argparse.ArgumentParser(description='Search Some files')
# action默认六个行为：
#   1）store:默认行为
#   2）store_const:保存默认参数
#   3）store_true/store_false: 保存相应的布尔值
#   4）append: 将值保存到列表中
#   5）append_const: 将const值append到列表中
#   6）version: 打印version信息
parser.add_argument(dest='filenames', metavar='filename', nargs='*')
# action:append,通过append将-p参数拼接到一起
parser.add_argument('-p', '--pat', metavar='pattern', required=True, dest='patterns', action='append',
                    help='text pattern to search for')
# action: store_true将保存相应的布尔值True, store_false将保存相应的布尔值False
parser.add_argument('-v', dest='verbose', action='store_true', help='verbose mode')
# action: store,默认行为
parser.add_argument('-o', dest='outfile', action='store', help='output file')
# action: store_const,保存默认的参数
parser.add_argument('-c', action='store_const', dest='const_value', const='value_const', help='store a const value')
# action: append_const,将constz值append到列表中
parser.add_argument('-A', action='append_const', dest='const_list', const='value-1', default=[])
parser.add_argument('-B', action='append_const', dest='const_list', const='value-2')
# choices: 限制参数的选择，默认slow
parser.add_argument('--speed', dest='speed', action='store', choices=('slow', 'fast'), default='slow', help='search apeed')
# action: version
parser.add_argument('--version', action='version', version='%(prog)s 1.0')

args = parser.parse_args()

print(args.filenames)
print(args.patterns)
print(args.const_value)
print(args.verbose)
print(args.speed)
print(args.const_list)
print(args.version)
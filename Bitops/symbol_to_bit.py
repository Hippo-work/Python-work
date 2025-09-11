from itertools import batched
import numpy as np

symbol_size = 3
symbol_order_1 = 0,1,2
symbol_order_2 = 0,2,1
symbol_order_3 = 1,0,2
data_symbols = [0,1,2,3,4,5,6,7,0]
print("Original ", data_symbols)


bat = batched(data_symbols, symbol_size)
data_rearranged = []
for b in bat:
    symbol_rearranged = [b[i] for i in symbol_order_2]
    data_rearranged.extend(symbol_rearranged)
print("0,2,1    ",data_rearranged)


data_rearranged = []
for sym in range(0,len(data_symbols), symbol_size):
    symbol = data_symbols[sym:sym+symbol_size]
    symbol_rearranged = [symbol[i] for i in symbol_order_3]
    data_rearranged.extend(symbol_rearranged)
print("1,0,2    ",data_rearranged)
    
    # symbol_np = [np.binary_repr(s, width=symbol_size) for s in symbol] #converts to bin

data_binrep = [np.binary_repr(b, width=symbol_size) for b in data_rearranged]
print(f"symbol to bin",data_binrep)
data_bit_list = [int(bit) for bits in data_binrep for bit in bits]
print("to bits  ",np.array(data_bit_list))


###convert to symbols from bits
# data_bit_list = [0,1,1,0,0,0,1,1,0,1,1,1,0,0,0,1,1,0] #3,0,6,7,0,6

data_bit_list_batched = batched(data_bit_list, symbol_size)
data_symbols_from_bits = []
for b in data_bit_list_batched:
    symbol = int("".join(map(str, b)), 2)
    data_symbols_from_bits.append(symbol)

print("From bits to symbols:", np.array(data_symbols_from_bits))
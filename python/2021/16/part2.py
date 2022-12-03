def product(nums):
    result = 1
    for num in nums:
        result *= num
    return result


def is_greater(nums):
    return int(nums[0] > nums[1])


def is_smaller(nums):
    return int(nums[0] < nums[1])


def is_equal(nums):
    return int(nums[0] == nums[1])


OP_MAP = {
    0: sum,
    1: product,
    2: min,
    3: max,
    5: is_greater,
    6: is_smaller,
    7: is_equal,
}


def hex_to_bin(hex_char):
    dec = int(hex_char, 16)
    return format(dec, '0>4b')


def create_packet_reader(packet):
    while True:
        hex_char = packet.read(1)
        bin_seq = hex_to_bin(hex_char)
        for digit in bin_seq:
            yield digit


def get_next_n_bits(num, iterable):
    return ''.join([next(iterable) for _ in range(num)])


def read_packet_literal(iterable):
    num = ''

    while int(next(iterable)):
        num += get_next_n_bits(4, iterable)
    num += get_next_n_bits(4, iterable)
    return int(num, 2)


def read_packet_operator(iterable, operation):
    length_type = int(next(iterable))
    values = []
    version_count = 0
    # print(f'{length_type=}')

    if not length_type:
        subpacket_length = int(get_next_n_bits(15, iterable), 2)
        # print(f'{subpacket_length=}')
        new_packet = iter(get_next_n_bits(subpacket_length, iterable))

        while True:
            try:
                value, version = read_packet(new_packet)
                values.append(value)
                version_count += version
            except StopIteration:
                break
    else:
        n_sub_packets = int(get_next_n_bits(11, iterable), 2)
        # print(f'{n_sub_packets=}')

        for _ in range(n_sub_packets):
            value, version, = read_packet(iterable)
            values.append(value)
            version_count += version
    result = OP_MAP[operation](values)
    return result, version_count
        

def read_packet(packet):
    version = int(get_next_n_bits(3, packet), 2)
    # print(f'{version=}')

    packet_type = int(get_next_n_bits(3, packet), 2)
    # print(f'{packet_type=}')

    if packet_type == 4:
        value = read_packet_literal(packet)
    else:
        value, ver_inc = read_packet_operator(packet, packet_type)
        version += ver_inc

    return value, version


with open('input.txt', 'r') as file:
    # NOTE: Must be a single packet on a single line. No line terminator
    packet_reader = create_packet_reader(file)
    result = read_packet(packet_reader)
    print(result)
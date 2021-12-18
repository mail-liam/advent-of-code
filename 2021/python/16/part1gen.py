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
    read_more = True
    num = ''

    while read_more:
        chunk = get_next_n_bits(5, iterable)
        if not int(chunk[0]):
            read_more = False
        num += chunk[1:]
    return int(num, 2), 0


def read_packet_operator(iterable):
    length_type = int(next(iterable))
    version_count = 0
    # print(f'{length_type=}')

    if not length_type:
        subpacket_length = int(get_next_n_bits(15, iterable), 2)
        # print(f'{subpacket_length=}')
        new_packet = iter(get_next_n_bits(subpacket_length, iterable))

        while True:
            try:
                _, version = read_packet(new_packet)
                version_count += version
            except StopIteration:
                break
        return None, version_count

    n_sub_packets = int(get_next_n_bits(11, iterable), 2)
    # print(f'{n_sub_packets=}')

    for _ in range(n_sub_packets):
        _, version, = read_packet(iterable)
        version_count += version
    return None, version_count
        

def read_packet(packet):
    version = int(get_next_n_bits(3, packet), 2)
    # print(f'{version=}')

    packet_type = int(get_next_n_bits(3, packet), 2)
    # print(f'{packet_type=}')

    operation = read_packet_literal if packet_type == 4 else read_packet_operator

    value, ver_inc = operation(packet)
    return value, version + ver_inc


with open('input.txt', 'r') as file:
    # NOTE: Must be a single packet on a single line. No line terminator
    packet_reader = create_packet_reader(file)
    result = read_packet(packet_reader)
    print(result)
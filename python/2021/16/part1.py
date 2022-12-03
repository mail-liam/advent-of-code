from os import read


def bin_converter(num):
    return bin(num)[2:]


def fix_packet(packet):
    '''bin() strips leading zeroes =('''
    while len(packet) % 4 != 0:
        packet = '0' + packet
    return packet


def read_packet_literal(sequence):
    CHUNK_SIZE = 5
    index = 0
    read_more = True
    num = ''
    # print(sequence)

    while read_more:
        chunk = sequence[index:index+CHUNK_SIZE]
        if not int(chunk[0]):
            read_more = False
        num += chunk[1:]
        index += CHUNK_SIZE
    # print(f'Index increase from literal: {index}')
    return int(num, 2), 0, index


def read_packet_operator(sequence):
    # print(sequence)
    length_type = int(sequence[0])
    version_count = 0
    # print(f'{length_type=}')

    if not length_type:
        subpacket_length = int(sequence[1:16], 2)
        # print(f'{subpacket_length=}')
        subpackets = sequence[16:]
        index = 0

        while index < subpacket_length:
            _, version, increment = read_packet(subpackets[index:])
            version_count += version
            index += increment
        assert index == subpacket_length
        return None, version_count, index + 16

    n_sub_packets = int(sequence[1:12], 2)
    # print(f'{n_sub_packets=}')
    index = 12
    for _ in range(n_sub_packets):
        _, version, increment = read_packet(sequence[index:])
        version_count += version
        index += increment
    return None, version_count, index
        

def read_packet(packet):
    # print('-----')
    version = int(packet[0:3], 2)
    # print(f'{version=}')
    packet_type = int(packet[3:6], 2)
    # print('Literal Packet' if packet_type == 4 else 'Operator Packet')
    index = 6

    operation = read_packet_literal if packet_type == 4 else read_packet_operator

    value, ver_inc, index_inc = operation(packet[index:])
    return value, version + ver_inc, index + index_inc  # Include header


with open('input.txt') as file:
    packets = [line.strip() for line in file.readlines()]


for packet in packets:
    print(packet)
    packet = fix_packet(bin_converter(int(packet, 16)))

    result = read_packet(packet)
    print(result)
import cirq
import numpy as np

# Функция для генерации случайных битов и базисов
def generate_bits_and_bases(length):
    bits = np.random.randint(0, 2, length)
    bases = np.random.randint(0, 2, length)
    return bits, bases

# Функция для измерения состояния в зависимости от базиса
def measure(bits, bases, alice_bases):
    measurements = []
    for i in range(len(bits)):
        if bases[i] == alice_bases[i]:  # Базы совпадают
            measurements.append(bits[i])  # Измеряем в правильном базисе
        else:
            measurements.append(np.random.randint(0, 2))  # Измеряем случайно
    return measurements

# Протокол BB84
def bb84_protocol(key_length):
    # Генерация битов и базисов для Алисы
    alice_bits, alice_bases = generate_bits_and_bases(key_length)

    # Генерация базисов для Боба
    bob_bases = np.random.randint(0, 2, key_length)

    # Создание квантового регистра
    qubits = [cirq.NamedQubit(f'q{i}') for i in range(key_length)]
    circuit = cirq.Circuit()

    # Подготовка состояния Алисы
    for i in range(key_length):
        if alice_bits[i] == 1:
            circuit.append(cirq.X(qubits[i]))  # Применяем NOT-гейт для установки бита в 1

        if alice_bases[i] == 1:
            circuit.append(cirq.H(qubits[i]))  # Применяем Hadamard-гейт для изменения базиса

    # Измерение
    circuit.append(cirq.measure(*qubits, key='result'))

    # Выполнение симуляции
    simulator = cirq.Simulator()
    result = simulator.run(circuit, repetitions=1)
    
    bob_measurements = result.measurements['result'][0]

    # Формируем ключ
    key = ''.join(str(alice_bits[i]) for i in range(key_length) if alice_bases[i] == bob_bases[i])
    
    return key, bob_measurements

if name == "__main__":
    key_length = 50  # Длина ключа для BB84
    key, bob_measurements = bb84_protocol(key_length)
    print("Secret key:         ", key)
    print("Bob's measurements:  ", ''.join(map(str, bob_measurements)))

    # Сохранение ключа в файл
    with open("quantum_key.txt", "w") as key_file:
        key_file.write(key)

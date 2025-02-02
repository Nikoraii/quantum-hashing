namespace QuantumProjects.QuantumHash {
    @EntryPoint()
    operation GetQuantumBit() : Result {
        use q = Qubit();

        H(q);

        let result = M(q);

        Reset(q);

        return result;
    }

    operation GenerateQuantumBits(count : Int) : Result[] {
        mutable results : (Result)[] = [];

        for i in 0 .. count - 1 {
            results += [GetQuantumBit()];
        }

        return results;
    }
}
import { Link } from "expo-router";
import { Pressable, Text, View } from "react-native";

export default function SelectMoveScreen() {
    return (
        <View style={{ flex: 1, backgroundColor: "#000", justifyContent: "center", padding: 24 }}>
            <Text style={{ color: "#fff", fontSize: 22, marginBottom: 20 }}>Hareket Seç</Text>

            <Link href="/detail/Squat" asChild>
                <Pressable style={styles.button}>
                    <Text style={styles.text}>Squat</Text>
                </Pressable>
            </Link>

            <Link href="/detail/Bridge" asChild>
                <Pressable style={styles.button}>
                    <Text style={styles.text}>Bridge</Text>
                </Pressable>
            </Link>
        </View>
    );
}

const styles = {
    button: {
        backgroundColor: "#111",
        borderRadius: 12,
        padding: 16,
        marginBottom: 12,
        borderColor: "#B0FF35",
        borderWidth: 1,
    },
    text: {
        color: "#fff",
        fontSize: 18,
    },
};

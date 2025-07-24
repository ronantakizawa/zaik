fn main() {
    // Skip risc0 build for now to focus on AI agent testing
    println!("cargo:rerun-if-changed=methods/");
}
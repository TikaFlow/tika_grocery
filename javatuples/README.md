English | [简体中文](README_CN.md)

# Java Tuples

A library to create and use tuples in Java.

# Origin and Belonging

This project is fully derived from the `javatuples` library version 1.2, provided by its original author. Here is the information about the ownership of `javatuples`:

- **Project Name**: javatuples
- **Version**: 1.2
- **Author**: [The JAVATUPLES team](https://www.javatuples.org/)
- **License**: Apache License 2.0
- **Source Code**: [javatuples/javatuples](https://github.com/javatuples/javatuples)
- **License File**: [LICENSE](LICENSE.txt)

# Instructions for Use

For the use of `javatuples`, it is recommended to reference the original library through `maven`.

## 1. Add Dependency

Add the following dependency to your project's `pom.xml` file:

```xml
<dependency>
    <groupId>org.javatuples</groupId>
    <artifactId>javatuples</artifactId>
    <version>{version}</version>
    <scope>compile</scope>
</dependency>
```

If you cannot access the `maven` repository, I also have the compiled `javatuples-1.2.jar` file.

### Step 1: Install the jar package to the maven repository

```bash
mvn install:install-file \
-Dfile=javatuples-1.2.jar \
-DgroupId=org.javatuples \
-DartifactId=javatuples \
-Dversion=1.2 \
-Dpackaging=jar
-DgeneratePom=true
```

### Step 2: Reference in your project

Add the following dependency to your project's `pom.xml` file:

```xml
<dependency>
    <groupId>org.javatuples</groupId>
    <artifactId>javatuples</artifactId>
    <version>1.2</version>
</dependency>
```

### Step 3: Update maven

```bash
mvn clean install
```

## 2. Use Tuple

Here's an example of how to use `javatuples`:

```java
import org.javatuples.*;

public class Main {
    public static void main(String[] args) {
        // Create a Tuple with two elements--Pair
        Pair<String, Integer> nameAge = Pair.with("Alice", 25);

        // Access Tuple elements
        String name = nameAge.getValue0(); // "Alice"
        int age = nameAge.getValue1(); // 25

        // Set Tuple elements
        // Since Tuple objects are immutable, you need to receive a new Tuple object
        Pair<String, Integer> nameAge2 = nameAge.setAt0("Bob");

        // Add elements to Tuple
        Triplet<String, String, Integer> nameCityAge = nameAge2.addAt1("New York");

        // Remove elements from Tuple
        Pair<String, String> nameCity = nameCityAge.removeFrom2();

        // Print Tuple
        System.out.println(nameCity); // [Bob, New York]
    }
}
```

For more usage methods and examples, please refer to the [official documentation](https://www.javatuples.org/apidocs/index.html) of `javatuples`.

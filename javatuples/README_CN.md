# Java Tuples

在Java中创建和使用元组的库。

# 来源和归属

本项目完全来自`javatuples`库的1.2版本，该库由其原作者提供。以下是关于`javatuples`的归属信息：

- **项目名称**：javatuples
- **版本**：1.2
- **作者**：[The JAVATUPLES team](https://www.javatuples.org/)
- **许可证**：Apache License 2.0
- **源代码**：[javatuples/javatuples](https://github.com/javatuples/javatuples)
- **许可证文件**：[LICENSE](LICENSE.txt)

# 使用说明

对于`javatuples`的使用，建议通过`maven`引用原始库。

## 1、添加依赖

在项目的`pom.xml`文件中添加以下依赖：

```xml
<dependency>
    <groupId>org.javatuples</groupId>
    <artifactId>javatuples</artifactId>
    <version>{version}</version>
    <scope>compile</scope>
</dependency>
```

如果无法从`maven`仓库获取，我这里也有编译后的`javatuples-1.2.jar`文件。

### 第一步：安装jar包到maven仓库

```bash
mvn install:install-file \
-Dfile=javatuples-1.2.jar \
-DgroupId=org.javatuples \
-DartifactId=javatuples \
-Dversion=1.2 \
-Dpackaging=jar
-DgeneratePom=true
```

### 第二步：在项目中引用

在项目的`pom.xml`文件中添加以下依赖：

```xml
<dependency>
    <groupId>org.javatuples</groupId>
    <artifactId>javatuples</artifactId>
    <version>1.2</version>
</dependency>
```

### 第三步：更新maven

```bash
mvn clean install
```

## 2、使用Tuple

下面是一个使用`javatuples`的例子：

```java
import org.javatuples.*;

public class Main {
    public static void main(String[] args) {
        // 创建一个包含两个元素的Tuple--Pair
        Pair<String, Integer> nameAge = Pair.with("Alice", 25);

        // 访问Tuple的元素
        String name = nameAge.getValue0(); // "Alice"
        int age = nameAge.getValue1(); // 25

        // 设置Tuple的元素
        // 由于Tuple对象不可变，所以需要接收新的Tuple对象
        Pair<String, Integer> nameAge2 = nameAge.setAt0("Bob");

        // 添加元素到Tuple
        Triplet<String, String, Integer> nameCityAge = nameAge2.addAt1("New York");

        // 从Tuple中删除元素
        Pair<String, String> nameCity = nameCityAge.removeFrom2();

        // 打印Tuple
        System.out.println(nameCity); // [Bob, New York]
    }
}
```

更多的使用方法和示例，请参考`javatuples`的[官方文档](https://www.javatuples.org/apidocs/index.html)。
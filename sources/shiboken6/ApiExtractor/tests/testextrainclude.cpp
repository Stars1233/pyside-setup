// Copyright (C) 2016 The Qt Company Ltd.
// SPDX-License-Identifier: LicenseRef-Qt-Commercial OR GPL-3.0-only WITH Qt-GPL-exception-1.0

#include "testextrainclude.h"
#include "testutil.h"

#include <abstractmetalang.h>
#include <complextypeentry.h>
#include <typesystemtypeentry.h>
#include <clangparser/triplet.h>

#include <QtCore/qversionnumber.h>
#include <QtTest/qtest.h>

using namespace Qt::StringLiterals;

void TestExtraInclude::testClassExtraInclude()
{
    const char cppCode[] = "struct A {};\n";
    const char xmlCode[] = "\
    <typesystem package='Foo'>\n\
        <value-type name='A'>\n\
            <extra-includes>\n\
                <include file-name='header.h' location='global'/>\n\
            </extra-includes>\n\
        </value-type>\n\
    </typesystem>\n";

    QScopedPointer<AbstractMetaBuilder> builder(TestUtil::parse(cppCode, xmlCode, false));
    QVERIFY(builder);
    AbstractMetaClassList classes = builder->classes();
    const auto classA = AbstractMetaClass::findClass(classes, "A");
    QVERIFY(classA);

    QList<Include> includes = classA->typeEntry()->extraIncludes();
    QCOMPARE(includes.size(), 1);
    QCOMPARE(includes.constFirst().name(), u"header.h");
}

void TestExtraInclude::testGlobalExtraIncludes()
{
    const char cppCode[] = "struct A {};\n";
    const char xmlCode[] = "\
    <typesystem package='Foo'>\n\
        <extra-includes>\n\
            <include file-name='header1.h' location='global'/>\n\
            <include file-name='header2.h' location='global'/>\n\
        </extra-includes>\n\
        <value-type name='A'/>\n\
    </typesystem>\n";

    QScopedPointer<AbstractMetaBuilder> builder(TestUtil::parse(cppCode, xmlCode, false));
    QVERIFY(builder);
    AbstractMetaClassList classes = builder->classes();
    QVERIFY(AbstractMetaClass::findClass(classes, "A"));

    auto *td = TypeDatabase::instance();
    TypeSystemTypeEntryCPtr module = td->defaultTypeSystemType();
    QVERIFY(module);
    QCOMPARE(module->name(), u"Foo");

    QList<Include> includes = module->extraIncludes();
    QCOMPARE(includes.size(), 2);
    QCOMPARE(includes.constFirst().name(), u"header1.h");
    QCOMPARE(includes.constLast().name(), u"header2.h");
}

void TestExtraInclude::testParseTriplet_data()
{
    QTest::addColumn<QString>("tripletString");
    QTest::addColumn<bool>("expectedOk");
    QTest::addColumn<Architecture>("expectedArchitecture");
    QTest::addColumn<Platform>("expectedPlatform");
    QTest::addColumn<bool>("expectedCompilerPresent");
    QTest::addColumn<Compiler>("expectedCompiler");
    QTest::addColumn<bool>("expectedPlatformVersionPresent");
    QTest::addColumn<QVersionNumber>("expectedPlatformVersion");
    QTest::addColumn<QByteArray>("expectedConverted"); // test back-conversion

    QTest::newRow("Invalid")
        << QString("Invalid"_L1)
        << false << Architecture::X64 << Platform::Linux << false << Compiler::Gpp
        << false << QVersionNumber{} << QByteArray{};

    QTest::newRow("Linux")
        << QString("x86_64-unknown-linux-gnu"_L1)
        << true << Architecture::X64 << Platform::Linux << false << Compiler::Gpp
        << false << QVersionNumber{}
        << "x86_64-unknown-linux-gnu"_ba;

    QTest::newRow("Poky Linux")
        << QString("aarch64-poky-linux"_L1)
        << true << Architecture::Arm64<< Platform::Linux << false << Compiler::Gpp
        << false << QVersionNumber{}
        << "arm64-unknown-linux"_ba;

    QTest::newRow("WindowsArm")
        << QString("aarch64-pc-windows-msvc19.39.0"_L1)
        << true << Architecture::Arm64 << Platform::Windows << true << Compiler::Msvc
        << false << QVersionNumber{}
        << "arm64-pc-windows-msvc"_ba;

    QTest::newRow("Apple")
        << QString("arm64-apple-macosx15.0.0"_L1)
        << true << Architecture::Arm64 << Platform::macOS << false << Compiler::Gpp
        << true << QVersionNumber{15, 0, 0}
        << "arm64-apple-macosx15.0.0"_ba;

    QTest::newRow("AndroidArm32")
        << QString("armv7a-none-linux-android5.1"_L1)
        << true << Architecture::Arm32 << Platform::Android << false << Compiler::Gpp
        << true << QVersionNumber{5, 1}
        << "armv7a-unknown-linux-android5.1"_ba;

    QTest::newRow("AndroidArm64")
        << QString("aarch64-none-linux-androideabi27.1"_L1)
        << true << Architecture::Arm64 << Platform::Android << false << Compiler::Gpp
        << true << QVersionNumber{27, 1}
        << "aarch64-unknown-linux-android27.1"_ba;

    QTest::newRow("iOS")
        << QString("arm64-apple-ios"_L1)
        << true << Architecture::Arm64 << Platform::iOS << false << Compiler::Gpp
        << false << QVersionNumber{}
        << "arm64-apple-ios"_ba;
}

void TestExtraInclude::testParseTriplet()
{
    QFETCH(QString, tripletString);
    QFETCH(bool, expectedOk);
    QFETCH(Architecture, expectedArchitecture);
    QFETCH(Platform, expectedPlatform);
    QFETCH(bool, expectedCompilerPresent);
    QFETCH(Compiler, expectedCompiler);
    QFETCH(bool, expectedPlatformVersionPresent);
    QFETCH(QVersionNumber, expectedPlatformVersion);
    QFETCH(QByteArray, expectedConverted);

    auto tripletO = Triplet::fromString(tripletString);

    QCOMPARE(tripletO.has_value(), expectedOk);
    if (expectedOk) {
        const Triplet &triplet = tripletO.value();
        QCOMPARE(triplet.architecture(), expectedArchitecture);
        QCOMPARE(triplet.platform(), expectedPlatform);
        if (expectedPlatformVersionPresent) {
            QCOMPARE(triplet.platformVersion().isNull(), expectedPlatformVersion.isNull());
            QCOMPARE(triplet.platformVersion(), expectedPlatformVersion);
        }
        if (expectedCompilerPresent)
            QCOMPARE(triplet.compiler(), expectedCompiler);
        QCOMPARE(triplet.toByteArray(), expectedConverted);
    }
}

QTEST_APPLESS_MAIN(TestExtraInclude)
